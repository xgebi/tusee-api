use actix_web::{get, web, HttpRequest, post, HttpMessage};
#[cfg(unix)]
use actix_web::{middleware, App, Error as ActixError, http, HttpResponse, HttpServer};
use actix_web::cookie::Cookie;
use actix_web::dev::HttpResponseBuilder;
use actix_web::error::BlockingError;
use actix_web::http::{header, StatusCode};
use argon2::{
    password_hash::{
        rand_core::OsRng,
        PasswordHash, PasswordHasher, PasswordVerifier, SaltString
    },
    Argon2
};
use diesel::associations::HasTable;
use handlebars::Handlebars;
use serde::{Deserialize, Serialize};
use serde_json;
use crate::models::user::User;
use crate::schema::tusee_users::dsl::tusee_users;
use josekit::{JoseError, jwe::{JweHeader, A128GCMKW}, jwt::{self, JwtPayload}};
use diesel::prelude::*;
use crate::models::*;
use diesel::r2d2::{self, Error as DbError, ConnectionManager};
use crate::auth::token::Token;
use crate::utilities::configuration::Configuration;
use std::time::{SystemTime, UNIX_EPOCH};
use diesel::insert_into;
use josekit::jwe::JweDecrypter;
use totp_rs::{Algorithm, TOTP};
use crate::schema::tusee_settings::dsl::tusee_settings;
use crate::schema::tusee_users::{display_name, email, password, totp_secret, user_uuid};
use uuid::Uuid;
use crate::errors::user_management_errors::{CredentialsError, RegistrationError};
use rand::{thread_rng, Rng};
use rand::distributions::Alphanumeric;
use crate::utilities::utilities::{decrypt_token, encrypt_token};

type DbPool = r2d2::Pool<ConnectionManager<PgConnection>>;

#[derive(Deserialize, Serialize, Debug, Clone)]
pub struct LoginInfo {
    username: String,
    password: String,
}

#[derive(Deserialize, Serialize, Debug, Clone)]
pub struct RegistrationInfo {
    username: String,
    password: String,
    name: String,
}

#[derive(Deserialize, Serialize, Debug, Clone)]
pub struct TotpToken {
    token: String,
}

const FIVE_MINUTES_SECS: u64 = 60 * 10;

pub(crate) async fn show_login_page(hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    let data = json!({
        "error": false,
    });
    let body = hb.render("login", &data).unwrap();

    HttpResponse::Ok().body(body)
}

pub(crate) async fn login_user(pool: web::Data<DbPool>, hb: web::Data<Handlebars<'_>>, info: web::Form<LoginInfo>) -> Result<HttpResponse, ActixError> {
    use crate::schema::tusee_users::dsl::*;
    // validate against database
    // use web::block to offload blocking Diesel code without blocking server thread
    let username = info.username.clone();
    let user: Result<QueryResult<User>, BlockingError<DbError>> = web::block(move || {
        let conn = pool.get().unwrap();
        let user = tusee_users.filter(email.eq(&username)).first::<User>(&conn);
        Ok(user)
    }).await;

    if let Ok(user_result) = user {
        println!("user_result");
        if let Ok(user_query) = user_result {
            println!("user_query");
            let hashed_password = PasswordHash::new(&*user_query.password).unwrap();
            if let Ok(_) = Argon2::default().verify_password(info.password.as_ref(), &hashed_password) {
                println!("verified");
                let my_claim = Token {
                    email: info.username.to_owned(),
                    password: info.password.to_owned(),
                    totp_verified: false,
                    expiry_date: SystemTime::now().duration_since(SystemTime::UNIX_EPOCH).unwrap().as_secs() * FIVE_MINUTES_SECS,
                };

                if let Ok(cookie) = encrypt_token(my_claim) {
                    println!("cookie is good, {:?}", &cookie);
                    // Prompt setting up TOTP two factor authentication during first login
                    if user_query.first_login {
                        println!("To first login");
                        let mut resp = HttpResponse::build(StatusCode::FOUND)
                            .header(http::header::LOCATION, "/totp-setup").finish();
                        if let Ok(_) = resp.add_cookie(&cookie) {
                            println!("{:?}", &resp);
                            return Ok(resp);
                        }
                    } else if user_query.uses_totp {
                        // add if for set up totp
                        return Ok(HttpResponse::build(StatusCode::FOUND)
                            .header(http::header::LOCATION, "/totp-verify")
                            .cookie(cookie)
                            .finish());
                    } else {
                        // Without totp
                        return Ok(HttpResponse::build(StatusCode::FOUND)
                            .cookie(cookie)
                            .header(http::header::LOCATION, "/dashboard").finish());
                    }
                } else {
                    println!("Cookie is no good");
                }
            }
        }
    }
    // return error login page

    let data = json!({
        "error": true,
    });
    let body = hb.render("login", &data).unwrap();

    Ok(HttpResponse::Ok().body(body))
}

pub(crate) async fn show_registration_page(req: HttpRequest, hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    let mut already_registered = false;
    let mut general_registration_error = false;
    if let Some(_) = req.query_string().to_string().find("err=already_registered") {
        already_registered = true;
    }
    if let Some(_) = req.query_string().to_string().find("err=database_error") {
        general_registration_error = true;
    }
    let data = json!({
        "error": general_registration_error,
        "alreadyRegisteredError": already_registered
    });
    let body = hb.render("registration", &data).unwrap();

    HttpResponse::Ok().body(body)
}

pub(crate) async fn process_registration(hb: web::Data<Handlebars<'_>>, pool: web::Data<DbPool>,  info: web::Form<RegistrationInfo>) -> HttpResponse {
    // check database if user exists
    let username = info.username.clone();
    let user_registered = web::block(move || {
        let conn = pool.get().unwrap();
        let found_user = tusee_users.filter( email.eq(&username)).first::<User>(&conn);

        if let Err(_) = found_user {
            let salt = SaltString::generate(&mut OsRng);
            // Argon2 with default params (Argon2id v19)
            let argon2 = Argon2::default();

            // Hash password to PHC string ($argon2id$v=19$...)
            let password_hash = argon2.hash_password((&info.password).as_ref(), &salt).unwrap().to_string();
            // TODO decide after MVP stage if this is the best approach
            let rand_string: String = thread_rng()
                .sample_iter(&Alphanumeric)
                .take(16)
                .map(char::from)
                .collect();
            let res = insert_into(tusee_users)
                .values((user_uuid.eq(Uuid::new_v4().to_string()), email.eq(&info.username), display_name.eq(&info.name), password.eq(password_hash), totp_secret.eq(rand_string)))
                .execute(&conn);

            if let Ok(_) = res {
                return Ok(());
            }
            return Err(RegistrationError::DatabaseError);
        }
        Err(RegistrationError::AlreadyRegistered)
    }).await;

    match user_registered {
        Ok(_) => {
            HttpResponse::Found().header(http::header::LOCATION, "/login").finish()
        }
        Err(blocking_error) => {
            match blocking_error {
                BlockingError::Error(registration_error) => {
                    match registration_error {
                        RegistrationError::AlreadyRegistered => {
                            HttpResponse::Found().header(http::header::LOCATION, "/register?err=already_registered").finish()
                        }
                        RegistrationError::DatabaseError => {
                            HttpResponse::Found().header(http::header::LOCATION, "/register?err=database_error").finish()
                        }
                    }
                }
                BlockingError::Canceled => {
                    HttpResponse::Found().header(http::header::LOCATION, "/register?err=database_error").finish()
                }
            }
        }
    }
}

pub(crate) async fn show_setup_totp_page(req: HttpRequest, hb: web::Data<Handlebars<'_>>, pool: web::Data<DbPool>) -> HttpResponse {
    let conf = Configuration::new();
    let mut qr_verification_failed = false;
    if let Some(_) = req.query_string().to_string().find("qrerr=") {
        qr_verification_failed = true;
    }
    println!("setup totp start");
    if let Ok(token) = decrypt_token(req) {
        println!("setup totp token is good");
        let qr_image = web::block(move || {
            let conn = pool.get().unwrap();
            if let Ok(secret) = tusee_users.select(totp_secret).filter(email.eq(&token.email)).first::<String>(&conn) {
                println!("setup totp got secret");
                let totp = totp_factory(secret);
                let qr_image_string =  format!("data:image/png;base64,{}", totp.get_qr(&token.email.as_str(), conf.get_url().as_str()).unwrap());
                println!("{:?}", &qr_image_string);
                return Ok(qr_image_string);
            }
            println!("setup totp shouldn't see this");
            Err(CredentialsError::FailedCreatingTotpQr)
        }).await;


        let data = json!({
            "verification_failed_error": qr_verification_failed,
            "qr_image": qr_image.unwrap(),
        });
        println!("{:?}", &data);
        let body = hb.render("setup_totp_page", &data).unwrap();

        return HttpResponse::Ok().body(body);
    }

    let data = json!({
        "error": false,
        "qr_error": qr_verification_failed,
    });
    let body = hb.render("setup_totp_page", &data).unwrap();

    HttpResponse::Ok().body(body)
}

pub(crate) fn process_totp_setup(pool: web::Data<DbPool>,  totp_token: web::Form<TotpToken>) -> HttpResponse {
    let conf = Configuration::new();
    let totp = totp_factory(conf.get_secret());
    if totp.check(&totp_token.token, SystemTime::now()
        .duration_since(SystemTime::UNIX_EPOCH).unwrap()
        .as_secs()) {
        return HttpResponse::Found().header(http::header::LOCATION, "/dashboard").finish();
    }
    let mut response = HttpResponse::new(StatusCode::UNAUTHORIZED);
    response.del_cookie("token");
    let mut response_builder = HttpResponse::build_from(response);
    response_builder.header(http::header::LOCATION, "/login").finish()
}

fn totp_factory(secret: String) -> TOTP {
    TOTP::new(
        Algorithm::SHA1,
        6,
        1,
        30,
        Vec::from(secret),
    )
}