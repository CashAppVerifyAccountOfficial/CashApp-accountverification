const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const fs = require('fs');
const crypto = require('crypto');

const app = express();
const port = 3000;
const dataFile = path.join(__dirname, '..', 'private-data', 'submissions.log');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(__dirname));

app.post('/submit', (req, res) => {
  const { username, password } = req.body;

  if (!username || !password) {
    return res.status(400).send('Username and password are required.');
  }

  const record = {
    username,
    password: crypto.createHash('sha256').update(password).digest('hex'),
    submittedAt: new Date().toISOString()
  };

  fs.mkdirSync(path.dirname(dataFile), { recursive: true });
  fs.appendFileSync(dataFile, JSON.stringify(record) + '\n');

  res.send('Saved securely.');
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
