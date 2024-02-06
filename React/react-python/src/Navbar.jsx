import React from 'react'
import "./Nabarstyles.css"


function Navbar() {

  
  return (
    <div className='Navbar-container'>
      <div className='truetalent-logo'>
        <img src="https://truetalent.io/static/media/logo.b9612289.svg" alt="" style={{width:'150px',height:'30px'}}/>
      </div>
      <div className='list'>
        <a href="" className='li-job job-a'>Job</a>
        <a href="" className='li-job gig-a'>Gig</a>
        <a href="" className='li-job gig-a'>Resume Maker</a>
      </div>
      <div className='login-btn'>
          <button type="button" className='navbar-login'>Login</button>
          <button type="button" className='navbar-register'>Register</button>
        </div>
    </div>
  )
}

export default Navbar