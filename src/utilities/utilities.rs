use diesel::prelude::*;
use diesel::pg::PgConnection;
use std::env;
use actix_web::cookie::Cookie;
use actix_web::{HttpMessage, HttpRequest};
use josekit::jwe::{A128GCMKW, JweHeader};
use josekit::jwt;
use josekit::jwt::JwtPayload;
use lettre::message::header::To;
use crate::auth::token::Token;
use crate::Configuration;
use crate::errors::user_management_errors::CredentialsError;

// Getting data out of encrypted JWT token
pub(crate) fn encrypt_token(token: Token) -> Result<Cookie<'static>, CredentialsError> {
    let conf = Configuration::new();
    let mut header = JweHeader::new();
    header.set_token_type("JWT");
    header.set_content_encryption("A128CBC-HS256");
    let mut payload = JwtPayload::new();
    payload.set_subject(serde_json::to_string(&token).unwrap());
    if let Ok(encrypter) = A128GCMKW.encrypter_from_bytes(conf.get_cookie_secret().as_bytes()) {
        if let Ok(jwt) = jwt::encode_with_encrypter(&payload, &header, &encrypter) {
            return Ok(Cookie::build("token", jwt)
                .path("/")
                .secure(true)
                .http_only(false) // this needs to be tested a bit more with fetch api
                .finish());
        }
    }
    Err(CredentialsError::FailedCreatingCookie)
}

pub(crate) fn decrypt_token(request: HttpRequest) -> Result<Token, CredentialsError> {
    let conf = Configuration::new();
    println!("{:?}", &request);
    if let Some(request_cookie) = request.cookie("token") {
        if let Ok(decrypter) = A128GCMKW.decrypter_from_bytes(conf.get_cookie_secret().as_bytes()) {
            let (payload, header) = jwt::decode_with_decrypter(&(request_cookie.value()), &decrypter).unwrap();
            let token: Token = serde_json::from_str(&payload.subject().unwrap()).unwrap();
            Ok(token)
        } else {
            Err(CredentialsError::FailedExtractingCookie)
        }
    } else {
        println!("There's no cookie");
        Err(CredentialsError::FailedExtractingCookie)
    }
}
