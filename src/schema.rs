table! {
    tusee_access_audit_log (entry_uuid) {
        entry_uuid -> Varchar,
        tusee_user -> Varchar,
        ip -> Varchar,
        event -> Varchar,
    }
}

table! {
    tusee_available_user_boards (board_uuid) {
        board_uuid -> Varchar,
        tusee_user -> Varchar,
        board -> Varchar,
    }
}

table! {
    tusee_boards (board_uuid) {
        board_uuid -> Varchar,
        name -> Nullable<Text>,
        description -> Nullable<Text>,
        owner -> Varchar,
    }
}

table! {
    tusee_encrypted_keys (key_uuid) {
        key_uuid -> Varchar,
        tusee_user -> Varchar,
        key -> Text,
    }
}

table! {
    tusee_permissions_audit_log (entry_uuid) {
        entry_uuid -> Varchar,
        tusee_user -> Varchar,
        ip -> Varchar,
        event -> Varchar,
    }
}

table! {
    tusee_scheduled_blocks (block_uuid) {
        block_uuid -> Varchar,
        task -> Varchar,
        start_time -> Text,
        end_time -> Text,
    }
}

table! {
    tusee_settings (settings_name) {
        settings_name -> Varchar,
        display_name -> Varchar,
        settings_value_type -> Varchar,
        settings_value -> Varchar,
    }
}

table! {
    tusee_tasks (task_uuid) {
        task_uuid -> Varchar,
        creator -> Varchar,
        board -> Varchar,
        description -> Text,
        updated -> Text,
        created -> Text,
    }
}

table! {
    tusee_users (user_uuid) {
        user_uuid -> Varchar,
        display_name -> Text,
        password -> Varchar,
        email -> Varchar,
        token -> Varchar,
        expiry_date -> Float8,
        first_login -> Bool,
        uses_totp -> Bool,
        totp_secret -> Varchar,
    }
}

joinable!(tusee_available_user_boards -> tusee_boards (board));
joinable!(tusee_scheduled_blocks -> tusee_tasks (task));
joinable!(tusee_tasks -> tusee_users (creator));

allow_tables_to_appear_in_same_query!(
    tusee_access_audit_log,
    tusee_available_user_boards,
    tusee_boards,
    tusee_encrypted_keys,
    tusee_permissions_audit_log,
    tusee_scheduled_blocks,
    tusee_settings,
    tusee_tasks,
    tusee_users,
);
