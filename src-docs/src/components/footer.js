import React from 'react'
import { Link } from 'gatsby'

import './footer.css'

const Footer = () => (
  <div>
    <div className="container">
      <div className="footer">
        <p className="copyright">Copyright &copy; 2019 Ewerton Carlos Assis</p>
      </div>
    </div>
    <div className="subfooter container">
      <div className="submenu">
        <ul className="inline-list">
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <a href="//carlosassis.com">Personal website</a>
          </li>
        </ul>
      </div>
      <div className="cookies-warning">
        <span>This website doesn't track you and it doesn't use cookies!</span>
      </div>
    </div>
  </div>
)

export default Footer
