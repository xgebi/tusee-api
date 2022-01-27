use actix_web::{get, web, HttpRequest, post};
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
use crate::models::user::User;
use crate::schema::tusee_users::dsl::tusee_users;
use jsonwebtoken::{encode, Algorithm, Header, EncodingKey};
use diesel::prelude::*;
use crate::models::*;
use diesel::r2d2::{self, Error as DbError, ConnectionManager};
use crate::utilities::configuration::Configuration;

type DbPool = r2d2::Pool<ConnectionManager<PgConnection>>;

#[derive(Deserialize, Serialize, Debug, Clone)]
pub struct LoginInfo {
    username: String,
    password: String,
}

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
                let my_claim = LoginInfo {
                    username: info.username.to_owned(),
                    password: info.password.to_owned()
                };
                let conf = Configuration::new();
                let jwttoken = encode(&Header::default(), &my_claim, &EncodingKey::from_secret(conf.get_secret().as_ref())).unwrap();
                let cookie = Cookie::build("token", jwttoken)
                    .domain(conf.get_url())
                    .path("/")
                    .secure(true)
                    .http_only(true) // this needs to be tested a bit more
                    .finish();

                let mut response = HttpResponse::new(StatusCode::FOUND);
                response.add_cookie(&cookie);
                let mut response_builder = HttpResponse::build_from(response);
                return Ok(response_builder.header(http::header::LOCATION, "/dashboard").finish());
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
