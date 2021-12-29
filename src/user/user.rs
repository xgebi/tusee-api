use std::error::Error;
use actix_web::{get, post, web::{self, Data, ServiceConfig}, HttpRequest, HttpResponse, Responder};
use postgres::Row;
use serde::{Deserialize, Serialize};
use serde_json::Result;
use bcrypt::{BcryptResult, DEFAULT_COST, hash, verify};
use crate::models::user::User;
use crate::schema::tusee_users::dsl::tusee_users;
use crate::schema::tusee_users::email;
use crate::utilities::utilities::establish_connection;

#[derive(Debug, Serialize)]
struct IsRegistrationEnabled {
    is_enabled: bool,
}

#[derive(Debug, Serialize, Deserialize)]
struct UserDetails {
    username: String,
    password: String
}

#[derive(Debug, Serialize)]
struct LoginResult {
    token: String,
    error: bool,
    error_message: String
}

#[derive(Debug, Serialize)]
struct RegistrationResult {
    error: bool,
    message: String,
}

#[get("/api/registration-enabled")]
pub(crate) async fn is_registration_enabled() -> HttpResponse {
    let res = HttpResponse::Ok()
        .json(IsRegistrationEnabled {
            is_enabled: true,
        });
    res
}

// #[post("/api/login")]
// pub(crate) async fn log_user_in(req_body: String) -> HttpResponse {
//     let user_details: UserDetails;
//     match serde_json::from_str(req_body.as_str()) {
//         Ok(ud) => {
//             user_details = ud;
//         }
//         Err(_) => {
//             return HttpResponse::Ok()
//                 .json(LoginResult {
//                     token: "".to_string(),
//                     error: true,
//                     error_message: "Could not login".to_string()
//                 });
//         }
//     }
//     let mut conn = create_database_connection();
//     let row = conn.query_one("SELECT password FROM tusee_users WHERE email={}", &[&user_details.username]);
//     let mut login_result: LoginResult;
//     match row {
//         Ok(r) => {
//             let password_hash: String = r.get(0);
//             let valid = verify(user_details.password.as_str(), &password_hash.as_str());
//             match valid {
//                 Ok(valid_result) => {
//                     if valid_result {
//                         login_result = LoginResult {
//                             token: "temporary token".to_string(),
//                             error: false,
//                             error_message: "".to_string()
//                         }
//                     } else {
//                         login_result = LoginResult {
//                             token: "".to_string(),
//                             error: true,
//                             error_message: "Could not login".to_string()
//                         };
//                     }
//                 }
//                 Err(_) => {
//                     login_result = LoginResult {
//                         token: "".to_string(),
//                         error: true,
//                         error_message: "Could not login".to_string(),
//                     };
//                 }
//             }
//         }
//         Err(_) => {
//             login_result = LoginResult {
//                 token: "".to_string(),
//                 error: true,
//                 error_message: "Could not login".to_string()
//             };
//         }
//     }
//
//     let res = HttpResponse::Ok()
//         .json(login_result);
//     res
// }

#[post("/api/register")]
pub(crate) async fn register_user(req_body: String) -> HttpResponse {
    let user_details: UserDetails;
    match serde_json::from_str(req_body.as_str()) {
        Ok(ud) => {
            user_details = ud;
        }
        Err(_) => {
            return HttpResponse::Ok()
                .json(RegistrationResult {
                    error: true,
                    message: "Could not register".to_string()
                });
        }
    }

    let mut conn = establish_connection();
    tusee_users.select(tusee_users::email).filter(tusee_users::email.eq);

    let mut registration_result: RegistrationResult = RegistrationResult { error: false, message: "".to_string() };
    // match row {
    //     Ok(r) => {
    //         if !r.is_empty() {
    //             registration_result = RegistrationResult {
    //                 error: true,
    //                 message: "Email already in use".to_string()
    //             }
    //         } else {
    //             let hashed_password = hash(user_details.password.as_str(), DEFAULT_COST)?;
    //         }
    //     }
    //     Err(_) => {
    //         registration_result = RegistrationResult {
    //             error: true,
    //             message: "Could not register".to_string()
    //         };
    //     }
    // }

    let res = HttpResponse::Ok()
        .json(registration_result);
    res
}