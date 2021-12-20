table! {
    tusee_users (uuid) {
        uuid -> Varchar,
        display_name -> Nullable<Text>,
        password -> Varchar,
        email -> Nullable<Varchar>,
        token -> Nullable<Varchar>,
        expiry_date -> Nullable<Float8>,
    }
}
