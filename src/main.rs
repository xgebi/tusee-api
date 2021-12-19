mod user;
mod services;
mod utilities;

use actix_web::{get, post, web, http, App, HttpResponse, HttpServer, Responder};
use actix_cors::Cors;
use lettre::transport::smtp::authentication::Credentials;
use lettre::{Message, SmtpTransport, Transport};
use crate::user::user::{log_user_in, register_user, is_registration_enabled};

#[post("/echo")]
async fn echo(req_body: String) -> impl Responder {
    HttpResponse::Ok().body(req_body)
}

async fn manual_hello() -> impl Responder {
    HttpResponse::Ok().body("Hey there!")
}

#[post("/send-email")]
async fn send_email(req_body: String) -> impl Responder {
    println!("Sending email");
    let email = Message::builder()
        .from("NoBody <nobody@domain.tld>".parse().unwrap())
        .reply_to("Yuin <yuin@domain.tld>".parse().unwrap())
        .to("Hei <hei@domain.tld>".parse().unwrap())
        .subject("Happy new year")
        .body(req_body)
        .unwrap();

    let creds = Credentials::new("smtp_username".to_string(), "smtp_password".to_string());

    // Open a remote connection to localhost
    let mailer = SmtpTransport::unencrypted_localhost();

    // Send the email
    return match mailer.send(&email) {
        Ok(_) => HttpResponse::Ok().body("Email sent"),
        Err(e) => HttpResponse::Ok().body(format!("Could not send email: {:?}", e)),
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .wrap(Cors::permissive().allowed_origin_fn(|origin, _req_head| {
                return match origin.to_str() {
                    Err(_) => false,
                    Ok(val) => val.find("localhost").is_some()
                }
            }))
            .service(echo)
            .service(send_email)
            .service(is_registration_enabled)
            .service(log_user_in)
            .service(register_user)
            .route("/hey", web::get().to(manual_hello))
    })
        .bind("127.0.0.1:8081")?
        .run()
        .await
}
