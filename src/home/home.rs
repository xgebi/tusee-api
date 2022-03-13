use actix_web::{middleware, App, HttpResponse, HttpServer, get, web, HttpRequest};
use handlebars::Handlebars;

pub(crate) async fn process_home(hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    // Check for jwt cookie
    // validate cookie
    // if cookie still valid -> redirect to dashboard
    // if invalid -> redirect to login
    // else render index page
    let data = json!({
        "name": "Handlebars"
    });
    println!("it's in processing home");
    let body = hb.render("index", &data).unwrap();

    HttpResponse::Ok().body(body)
}