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
use image::Luma;
use josekit::jwe::JweDecrypter;
use otpauth::TOTP;
use qrcode::QrCode;

type DbPool = r2d2::Pool<ConnectionManager<PgConnection>>;

#[derive(Deserialize, Serialize, Debug, Clone)]
pub struct LoginInfo {
    username: String,
    password: String,
}

const FIVE_MINUTES_SECS: u64 = 60 * 10;

#[get("/login")]
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
        if let Ok(user_query) = user_result {
            let hashed_password = PasswordHash::new(&*user_query.password).unwrap();
            if let Ok(_) = Argon2::default().verify_password(info.password.as_ref(), &hashed_password) {
                let my_claim = Token {
                    email: info.username.to_owned(),
                    password: info.password.to_owned(),
                    mfa_verified: false,
                    expiry_date: SystemTime::now().duration_since(SystemTime::UNIX_EPOCH).unwrap().as_secs() * FIVE_MINUTES_SECS,
                };
                let conf = Configuration::new();
                let mut header = JweHeader::new();
                header.set_token_type("JWT");
                header.set_content_encryption("A128CBC-HS256");

                let mut payload = JwtPayload::new();
                payload.set_subject(serde_json::to_string(&my_claim).unwrap());

                // Encrypting JWT
                if let Ok(encrypter) = A128GCMKW.encrypter_from_bytes(conf.get_secret().as_bytes()) {
                    if let Ok(jwt) = jwt::encode_with_encrypter(&payload, &header, &encrypter) {
                        let cookie = Cookie::build("token", jwt)
                            .domain(conf.get_url())
                            .path("/")
                            .secure(true)
                            .http_only(true) // this needs to be tested a bit more with fetch api
                            .finish();

                        let mut response = HttpResponse::new(StatusCode::FOUND);
                        if let Ok(_) = response.add_cookie(&cookie) {
                            let mut response_builder = HttpResponse::build_from(response);
                            // Prompt setting up TOTP two factor authentication during first login
                            if user_query.first_login {
                                return Ok(response_builder.header(http::header::LOCATION, "/setup-totp").finish());
                            }
                            // add if for set up totp
                            return Ok(response_builder.header(http::header::LOCATION, "/check-totp").finish());
                            // Without totp
                            return Ok(response_builder.header(http::header::LOCATION, "/dashboard").finish());
                        }
                    }
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

pub(crate) async fn show_registration_page(hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    let already_registered = false;
    let general_registration_error = false;
    // check whether user is already registered
    // if not register user
    // after successful registration redirect to login
    let data = json!({
        "error": general_registration_error,
        "alreadyRegisteredError": already_registered
    });
    let body = hb.render("registration", &data).unwrap();

    HttpResponse::Ok().body(body)
}

pub(crate) async fn process_registration(hb: web::Data<Handlebars<'_>>, pool: web::Data<DbPool>) -> HttpResponse {
    let data = json!({
        "error": false,
        "alreadyRegisteredError": false
    });
    let body = hb.render("registration_processed", &data).unwrap();

    HttpResponse::Ok().body(body)
}

pub(crate) async fn show_setup_totp_page(req: HttpRequest, hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    let conf = Configuration::new();
    if let Some(request_cookie) = req.cookie("token") {
        if let Ok(decrypter) = A128GCMKW.decrypter_from_bytes(conf.get_secret().as_bytes()) {
            let (payload, header) = jwt::decode_with_decrypter(&request_cookie, &decrypter).unwrap();
            println!("{}", payload.subject);
            let auth = TOTP::new(conf.get_secret());
            let qr_image = format!("data:image/png;base64,{}", auth.to_uri("", conf.get_url().as_str()));
        }
    }

    let data = json!({
        "error": false,
    });
    let body = hb.render("setup_totp_page", &data).unwrap();

    HttpResponse::Ok().body(body)
}

fn create_qr_image(to_encode: String) -> String {
    let code = QrCode::new(&to_encode)?;
    let mut vec = Vec::new();
    let encoder = image::png::PngEncoder::new(&mut vec);
    encoder.encode(
        code.render::<Luma<u8>>().build().as_ref(),
        ((code.width() + 8) * 8) as u32,
        ((code.width() + 8) * 8) as u32,
        image::ColorType::L8,
    )?;
    base64::encode(vec)
}