//! ${project_name} - A Rust library

pub fn hello(name: &str) -> String {
    format!("Hello, {}!", name)
}

pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hello() {
        assert_eq!(hello("World"), "Hello, World!");
    }

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
        assert_eq!(add(-1, 1), 0);
    }
}