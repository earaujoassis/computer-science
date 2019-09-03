import React from 'react'
import PropTypes from 'prop-types'
import Helmet from 'react-helmet'
import { StaticQuery, graphql } from 'gatsby'

import Header from './header'
import Footer from './footer'
import './layout.css'
import './pages.css'

const Layout = ({ children }) => (
  <StaticQuery
    query={graphql`
      query SiteTitleQuery {
        site {
          siteMetadata {
            title
          }
        }
      }
    `}
    render={data => (
      <>
        <Helmet
          title={data.site.siteMetadata.title}
          meta={[
            { name: 'description', content: 'Personal website by Ewerton Carlos Assis, Senior Software Engineer and Computer Scientist' },
            { name: 'keywords', content: 'personal, website, computer scientist, software engineer' },
          ]}
        >
          <html lang="en" />
          <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,400i|Vollkorn:600,600i" rel="stylesheet" />
        </Helmet>
        <Header />
        <div className="container root">
          {children}
        </div>
        <Footer />
      </>
    )}
  />
)

Layout.propTypes = {
  children: PropTypes.node.isRequired,
}

export default Layout
