import './NewsCard.css';

import React from 'react';

class NewsCard extends React.Component {


  // open a new tab for the URL
  redirectToUrl(url, event) {
      event.preventDefault();
      window.open(url, '_blank');
  }

  render() {
    return (
      <div className='news-container' onClick={
        (e) => this.redirectToUrl(this.props.news.url, e)
      }>
        <div className='row'>
          {/* news image */}
          <div className='col s4 fill'>
            <img src={this.props.news.urlToImage} alt='news' />
          </div>
          {/* news title and description */}
          <div className='col s8'>
            <div className='news-intro-col'>
              <div className='news-intro-panel'>
                <h4>{this.props.news.title}</h4>
                <div className='news-description'>
                  <p>{this.props.news.description}</p>
                  <div>
                    {/* optional news labels */}
                    {this.props.news.source != null
                      && <div className='chip light-blue news-chip'>
                          {this.props.news.source}</div>}
                    {this.props.news.reason != null
                      && <div className='chip light-green news-chip'>
                          {this.props.news.reason}</div>}
                    {this.props.news.time != null
                      && <div className='chip amber news-chip'>
                          {this.props.news.time}</div>}

                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }



}

export default NewsCard
