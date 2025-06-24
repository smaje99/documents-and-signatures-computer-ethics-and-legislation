def main() -> None:
    import uvicorn
    from app.app import app

    uvicorn.run(app, reload=True)


if __name__ == "__main__":
    main()
