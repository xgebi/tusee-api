table! {
    tusee_settings (settings_name) {
        settings_name -> Varchar,
        display_name -> Varchar,
        settings_value_type -> Tusee_settings_type,
        settings_value -> Varchar,
    }
}

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

allow_tables_to_appear_in_same_query!(
    tusee_settings,
    tusee_users,
);
