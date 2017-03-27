var app = new Vue({
  delimiters: ['${', '}'],
  el: '#tweets',
  data: {
    tweets: [],
  },
  created: function() {
    this.$http.get('http://' + API_URL + '/tweets').then(function (response) {
        this.tweets = response.body;
    });
    var ws = new WebSocket('ws://' + API_URL + '/tweets/ws');
    var that = this;
    ws.onmessage = function (event) {
        that.tweets.unshift(JSON.parse(event.data));
    }
  }
});