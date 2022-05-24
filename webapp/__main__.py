if __name__ == '__main__':
    import uvicorn

    from conf.config import settings

    uvicorn.run(
        'webapp.main:create_app',
        host=settings.BIND_IP,
        port=settings.BIND_PORT,
        reload=True,
    )
