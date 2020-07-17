require('dotenv').config()
const redis = require("redis");
const mongoose = require('mongoose');
const app = require('express')();
const http = require('http').createServer(app);
const subscriber = redis.createClient();
const io = require('socket.io')(http, {
  test: "hello"
});

// MongoDB

mongoose.connect(process.env.MONGODB_URL, { useNewUrlParser: true, useUnifiedTopology: true });

const Tick = mongoose.model('Tick', {
  symbol: {
    type: String,
    index: true,
    unique: true
  }, bid: Number, ask: Number, updated_at: {
    type: Date,
    default: Date.now()
  }
});

subscriber.on("message", (channel, msg) => {

  const message = JSON.parse(msg)

  // Save Tick to Database
  // Find If symbol if exist
  Tick.findOne({ symbol: message.symbol }, (err, tick) => {

    if (!tick) {

      const tick = Tick({
        symbol: message.symbol,
        bid: message.bid,
        ask: message.ask
      })
      tick.save()
    } else {
      tick.bid = message.bid
      tick.ask = message.ask
      tick.save()
    }

  })

  // Emit tick to socket.io
  io.emit("quote", {
    symbol: message.symbol,
    bid: message.bid,
    ask: message.ask
  })

});

subscriber.subscribe("quote");

io.on('connection', (socket) => {
  
  // Sent Initial Prices
  const ticks = Tick.find({})
  ticks.then((tick) => {
    socket.emit("initial_quote", tick)
  })
})

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

http.listen(3000, () => {
  console.log('listening on *:3000');
});