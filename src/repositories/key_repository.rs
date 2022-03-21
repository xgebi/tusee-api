use diesel::{PgConnection, QueryResult};
use diesel::r2d2::{ConnectionManager, PooledConnection};
use diesel::insert_into;
use uuid::Uuid;
use diesel::prelude::*;
use crate::auth::forms::RegistrationInfo;
use crate::models::*;
use crate::schema::tusee_encrypted_keys::dsl::tusee_encrypted_keys;
use crate::schema::tusee_encrypted_keys::{key_uuid, tusee_user, key};

pub(crate) fn insert_key(conn: &PooledConnection<ConnectionManager<PgConnection>>, user_uuid: &String, encrypted_key: &String) -> QueryResult<usize> {
    let res = insert_into(tusee_encrypted_keys)
        .values((key_uuid.eq(Uuid::new_v4().to_string()), tusee_user.eq(&user_uuid), key.eq(&encrypted_key)))
        .execute(conn);
    res
}