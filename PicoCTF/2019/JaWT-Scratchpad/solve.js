const jwt = require('jsonwebtoken');
const secretKey = 'ilovepico';

const token = jwt.sign({
    user: 'admin',
}, secretKey);

console.log(token);