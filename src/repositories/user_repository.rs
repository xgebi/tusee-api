use diesel::{PgConnection, QueryResult};
use diesel::r2d2::{ConnectionManager, PooledConnection};
use diesel::insert_into;
use crate::schema::tusee_users::dsl::tusee_users;
use crate::schema::tusee_users::{display_name, email, password, user_uuid};
use uuid::Uuid;
use diesel::prelude::*;
use crate::auth::forms::RegistrationInfo;
use crate::models::*;

pub(crate) fn insert_user(conn: &PooledConnection<ConnectionManager<PgConnection>>, info: &RegistrationInfo, password_hash: String, id: &String) -> QueryResult<usize> {
    let res = insert_into(tusee_users)
        .values((user_uuid.eq(&id), email.eq(&info.username), display_name.eq(&info.name), password.eq(password_hash)))
        .execute(conn);
    res
}