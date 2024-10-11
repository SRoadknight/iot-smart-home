db.createUser({
    user: 'admin',
    pwd: 'secret',
    roles: [
        {
            role: 'root',
            db: 'admin'
        }
    ]
});