import React from 'react'
import { Link } from 'gatsby'

import Layout from '../components/layout'

const NotFoundPage = () => (
  <Layout>
    <h1>Oops... page not found</h1>
    <p>The content you're looking for doesn't exist. Perhaps you may try from the <Link to="/">index page</Link></p>
  </Layout>
)

export default NotFoundPage
