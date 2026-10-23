use axum::{
    routing::{get, post},
    http::StatusCode,
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use tower_http::cors::{Any, CorsLayer};

#[derive(Serialize)]
struct HealthResponse {
    status: String,
}

#[derive(Deserialize, Serialize)]
struct Item {
    name: String,
    description: Option<String>,
    price: f64,
    quantity: i32,
}

async fn health() -> Json<HealthResponse> {
    Json(HealthResponse { status: "ok".to_string() })
}

async fn root() -> &'static str {
    "Welcome to ${project_name}"
}

async fn create_item(Json(item): Json<Item>) -> (StatusCode, Json<Item>) {
    (StatusCode::CREATED, Json(item))
}

async fn get_item(axum::extract::Path(id): axum::extract::Path<i32>) -> Json<serde_json::Value> {
    Json(serde_json::json!({ "item_id": id, "name": format!("Item {}", id) }))
}

#[tokio::main]
async fn main() {
    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    let app = Router::new()
        .route("/", get(root))
        .route("/health", get(health))
        .route("/items", post(create_item))
        .route("/items/:id", get(get_item))
        .layer(cors);

    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    println!("Server running on http://{}", addr);
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}