const express = require("express");
const axios = require("axios");

const USER_SERVICE = process.env.USER_SERVICE || "http://user-service:5002";
const TICKET_SERVICE = process.env.TICKET_SERVICE || "http://ticket-service:5001";

const app = express();
app.use(express.json());

app.get("/", async (req, res) => {
    const users = await axios.get(`${USER_SERVICE}/users`).then(r => r.data).catch(() => []);
    const tickets = await axios.get(`${TICKET_SERVICE}/tickets`).then(r => r.data).catch(() => []);
    
    const html = `
    <h1>Ticketing System</h1>
    
    <h2>Users</h2>
    <ul>${users.map(u => `<li>${u.username}</li>`).join("")}</ul>
    
    <h2>Tickets</h2>
    <ul>${tickets.map(t => `<li>${t.title} (${t.status})</li>`).join("")}</ul>

    <p>API Services Running ✅</p>
    `;
    
    res.send(html);
});

app.listen(8080, () => console.log("UI running on :8080"));
