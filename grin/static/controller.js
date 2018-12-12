
// get params      
function params(data) {
  return Object.keys(data).map(key => `${key}=${encodeURIComponent(data[key])}`).join('&');
}


// consumption of REST WS    
sendData = (endpoint, method, data = null) => {
  var config = {
    method: method,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }
  if(method == 'POST'){
      config.body = params(data)
  }
  return fetch(endpoint, config).then(res => res.json()).then(json => json)
}

      