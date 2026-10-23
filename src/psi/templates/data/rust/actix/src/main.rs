use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use serde::{Deserialize, Serialize};

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

async fn health() -> impl Responder {
    HttpResponse::Ok().json(HealthResponse { status: "ok".to_string() })
}

async fn root() -> impl Responder {
    HttpResponse::Ok().body("Welcome to ${project_name}")
}

async fn create_item(item: web::Json<Item>) -> impl Responder {
    HttpResponse::Created().json(item.into_inner())
}

async fn get_item(path: web::Path<i32>) -> impl Responder {
    let id = path.into_inner();
    HttpResponse::Ok().json(serde_json::json!({ "item_id": id, "name": format!("Item {}", id) }))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("Server running on http://127.0.0.1:8080");
    HttpServer::new(|| {
        App::new()
            .route("/", web::get().to(root))
            .route("/health", web::get().to(health))
            .route("/items", web::post().to(create_item))
            .route("/items/{id}", web::get().to(get_item))
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}