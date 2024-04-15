import Cookies from 'js-cookie'



  async function checkExpiredSession(hostname){
    const token = Cookies.get("user_token")
    if (token === undefined){
      alert("You need to be login")
    }
    return await fetch(`${hostname}/token/${token}`, {
      method: "GET",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    }).then( (response) => {
      return response.json()
    }).then( (data) => {
      if (data.status !== 200){
        alert("Your session is expired, please login again")

      }
      return data
    })
  }

export default {
  checkExpiredSession
}