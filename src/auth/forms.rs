use actix_web::{get, web, HttpRequest, post};
#[cfg(unix)]
use actix_web::{middleware, App, Error as ActixError, HttpResponse, HttpServer};
use actix_web::error::BlockingError;
use actix_web::http::{header};
use diesel::associations::HasTable;
use handlebars::Handlebars;
use serde::{Deserialize, Serialize};
use crate::models::user::User;
use crate::schema::tusee_users::dsl::tusee_users;
use crate::utilities::utilities::establish_connection;
use diesel::prelude::*;
use crate::models::*;
use diesel::r2d2::{self, Error as DbError, ConnectionManager};

type DbPool = r2d2::Pool<ConnectionManager<PgConnection>>;

#[derive(Deserialize, Serialize, Debug, Clone)]
pub struct LoginInfo {
    username: String,
    password: String,
}

#[get("/login")]
pub(crate) async fn show_login_page(hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    // Check for jwt cookie
    // validate cookie
    // if cookie still valid -> redirect to dashboard
    // if invalid -> redirect to login
    // else render index page
    let data = json!({
        "error": false,
    });
    println!("it's in processing home");
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
            if let Ok(password_verified) = bcrypt::verify(&info.password, &user_query.password) {
                // return good result
            }
        }
    }
    // return error login page

    Ok(HttpResponse::Ok().finish())
}
