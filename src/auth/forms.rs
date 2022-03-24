use std::error::Error;
use actix_web::{middleware, App, http, get, web, post, HttpResponse, HttpServer, HttpResponseBuilder, HttpRequest, HttpMessage};
use actix_web::cookie::Cookie;
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
use serde::{Deserialize, Serialize};
use serde_json;
use crate::models::user::User;
use crate::schema::tusee_users::dsl::tusee_users;
use josekit::{JoseError, jwe::{JweHeader, A128GCMKW}, jwt::{self, JwtPayload}};
use diesel::prelude::*;
use crate::models::*;
use diesel::r2d2::{self, Error as DbError, ConnectionManager, Pool};
use crate::auth::token::Token;
use crate::utilities::configuration::Configuration;
use std::time::{SystemTime, UNIX_EPOCH};
use diesel::insert_into;
use josekit::jwe::JweDecrypter;
use totp_rs::{Algorithm, TOTP};
use crate::schema::tusee_settings::dsl::tusee_settings;
use crate::schema::tusee_users::{display_name, email, password, user_uuid};
use uuid::Uuid;
use crate::errors::user_management_errors::{CredentialsError, RegistrationError};
use rand::{thread_rng, Rng};
use rand::distributions::Alphanumeric;
use crate::repositories::key_repository::insert_key;
use crate::utilities::utilities::{decrypt_token, encrypt_token};
use crate::repositories::user_repository::insert_user;

type DbPool = r2d2::Pool<ConnectionManager<PgConnection>>;

#[derive(Deserialize, Serialize, Debug, Clone)]
pub struct LoginInfo {
    username: String,
    password: String,
}

#[derive(Deserialize, Serialize, Debug, Clone)]
pub(crate) struct RegistrationInfo {
    pub(crate) username: String,
    pub(crate) password: String,
    pub(crate) name: String,
    pub(crate) key: String,
}

#[derive(Deserialize, Serialize, Debug, Clone)]
pub struct TotpToken {
    code: String,
}

const FIVE_MINUTES_SECS: u64 = 60 * 10;

pub(crate) async fn login_user(db: web::Data<DbPool>, info: web::Json<LoginInfo>) -> Result<HttpResponse, BlockingError> {
    use crate::schema::tusee_users::dsl::*;
    // validate against database
    // use web::block to offload blocking Diesel code without blocking server thread
    println!("{:?}", &info);
    let username = info.username.clone();
    let user= web::block(move || {
        let conn = db.get().unwrap();
        let user = tusee_users.filter(email.eq(&username)).first::<User>(&conn);
        user
    }).await?;

    if let Ok(user_result) = user {
        println!("user_query");
        let hashed_password = PasswordHash::new(&*user_result.password).unwrap();
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
                if user_result.first_login {
                    println!("To first login");
                    let mut resp = HttpResponse::build(StatusCode::FOUND).finish();
                    if let Ok(_) = resp.add_cookie(&cookie) {
                        return Ok(resp);
                    }
                } else if user_result.uses_totp {
                    // add if for set up totp
                    let mut resp = HttpResponse::build(StatusCode::FOUND).finish();
                    if let Ok(_) = resp.add_cookie(&cookie) {
                        println!("{:?}", &resp);
                        return Ok(resp);
                    }
                } else {
                    // Without totp
                    let mut resp = HttpResponse::build(StatusCode::FOUND).finish();
                    return Ok(resp);
                }
            } else {
                println!("Cookie is no good");
            }
        }
    }
    // return error login page

    Ok(HttpResponse::Ok().finish())
}

pub(crate) async fn process_registration(req: HttpRequest, db: web::Data<DbPool>, info: web::Json<RegistrationInfo>) -> HttpResponse {

    HttpResponse::Ok().finish()
    // // check database if user exists info: web::Json<RegistrationInfo>
    // println!("{:?}", &info);
    // let username = info.username.clone();
    // let user_registered = web::block(move || {
    //     let conn = db.get().unwrap();
    //     let found_user = tusee_users.filter( email.eq(&username)).first::<User>(&conn);
    //
    //     if let Err(_) = found_user {
    //         let salt = SaltString::generate(&mut OsRng);
    //         // Argon2 with default params (Argon2id v19)
    //         let argon2 = Argon2::default();
    //
    //         // Hash password to PHC string ($argon2id$v=19$...)
    //         let password_hash = argon2.hash_password((&info.password).as_ref(), &salt).unwrap().to_string();
    //         // TODO decide after MVP stage if this is the best approach
    //         // let rand_string: String = thread_rng()
    //         //     .sample_iter(&Alphanumeric)
    //         //     .take(16)
    //         //     .map(char::from)
    //         //     .collect();
    //         let id = Uuid::new_v4().to_string();
    //         if let Ok(_) = insert_user(&conn, &info, password_hash, &id) {
    //             if let Ok(_) = insert_key(&conn, &id, &info.key) {
    //                 return Ok(());
    //             }
    //         }
    //         return Err(RegistrationError::DatabaseError);
    //     }
    //     Err(RegistrationError::AlreadyRegistered)
    // }).await;
    //
    // match user_registered {
    //     Ok(result) => {
    //         match result {
    //             Ok(_) => {
    //                 HttpResponse::Found().finish()
    //             }
    //             Err(err) => {
    //                 match err {
    //                     RegistrationError::AlreadyRegistered => {
    //                         HttpResponse::Found().finish()
    //                     }
    //                     RegistrationError::DatabaseError => {
    //                         HttpResponse::Found().finish()
    //                     }
    //                 }
    //             }
    //         }
    //     }
    //     Err(_) => {
    //         HttpResponse::Found().finish()
    //     }
    // }
}

pub(crate) async fn process_totp_setup(req: HttpRequest, db: web::Data<DbPool>,  totp_token: web::Form<TotpToken>) -> HttpResponse {
    let conf = Configuration::new();
    let totp = totp_factory(conf.get_secret());
    println!("{:?}", &totp_token.code);
    let res_check = totp.check(&totp_token.code, SystemTime::now()
        .duration_since(SystemTime::UNIX_EPOCH).unwrap()
        .as_secs());
    println!("{}", res_check);
    if res_check {
        // TODO update first_login to false
        return HttpResponse::Found().append_header((http::header::LOCATION, "/dashboard")).finish();
    }
    let mut response = HttpResponse::Unauthorized();
    if let Some(mut cookie) = req.cookie("token") {
        cookie.make_removal();
        return response.cookie(cookie).append_header((http::header::LOCATION, "/login?error=totp")).finish();

    }
    response.append_header((http::header::LOCATION, "/login?error=totp")).finish()
}

fn totp_factory(secret: String) -> TOTP {
    let totp = TOTP::new(
        Algorithm::SHA1,
        6,
        1,
        30,
        Vec::from(secret),
    );
    totp
}