import './NewsCard.css';

import Auth from '../Auth/Auth'
import React from 'react';

class NewsCard extends React.Component {


  // open a new tab for the URL, and send click log
  redirectToUrl(url, event) {
      event.preventDefault();
      this.sendClickLog();
      window.open(url, '_blank');
  }

  // send user click log to server
  sendClickLog() {
    const url = 'http://' + window.location.hostname + ':3000'
      + '/news/userId/' + Auth.getEmail() + '/newsId/' + this.props.news.digest;
    // encode URI in case digest may contain non UTF-8 chars
    const request = new Request(
      encodeURI(url),
      {
        method: 'POST',
        headers: {'Authorization': 'bearer ' + Auth.getToken()},
      }
    );
    // send request, no response to deal with
    fetch(request);
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
