import React from 'react'

import Layout from '../components/layout'

const IndexPage = () => (
  <Layout>
    <h1>Computer Science projects &amp; research</h1>
    <p>Following is a list of projects &amp; research assets available in this repository</p>
    <ul>
      <li>
        <div className="entry">
          <p>Articles</p>
          <ul>
            <li>Comming soon...</li>
          </ul>
        </div>
      </li>
      <li>
        <div className="entry">
          <p>Graduate works</p>
          <ul>
            <li>Comming soon...</li>
          </ul>
        </div>
      </li>
      <li>
        <div className="entry">
          <p>Undergraduate works</p>
          <ul>
            <li>Monograph: <em>&ldquo;Heurísticas e metaheurísticas aplicadas ao Problema de Escalonamento Job-Shop:
              Um algoritmo evolucionário híbrido baseado na fertilização in vitro para solucionar problemas de
              escalonamento job-shop&rdquo;</em> (<a href="https://github.com/earaujoassis/computer-science/tree/master/undergraduate-works/monograph">full
              project</a>, <a href="https://github.com/earaujoassis/computer-science/blob/master/undergraduate-works/monograph/monograph/monograph.pdf">full text in Brazilian Portuguese</a>)</li>
          </ul>
        </div>
      </li>
    </ul>
  </Layout>
)

export default IndexPage
