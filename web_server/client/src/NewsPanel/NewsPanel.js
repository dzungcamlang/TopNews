import './NewsPanel.css';
import NewsCard from '../NewsCard/NewsCard';
import React from 'react';

class NewsPanel extends React.Component {
  constructor() {
    super();

    this.state = {news: null};
  }

  componentDidMount() {
    this.loadMoreNews();
  }

  render() {
    if (this.state.news) {
      return (
        <div>
          {this.renderNews()}
        </div>
      );
    } else {
      return (
        <div id='msg-app-loading'>
          Loading...
        </div>
      );
    }

  }


  renderNews() {
    // DOM element: list of all news cards
    const news_card_list = this.state.news.map(one_news => {
      return (
        // key attribute is provided for virtual DOM to render quickly
        <a className='list-group-item' key={one_news.digest}
          href='#'>
          <NewsCard news={one_news} />
        </a>
      );
    });

    // return nicely wrapped news card list
    return (
      <div className='container-fluid'>
        <div className='list-group'>
          {news_card_list}
        </div>
      </div>
    );
  }

  loadMoreNews() {
    const mock_news = [
      {
      "source": "The Wall Street Journal",
      "title": "Berkshire Hathaway Benefits From US Tax Plan",
      "description": "Berkshire Hathaway posted a $29 billion gain in 2017 related to changes in U.S. tax law, a one-time boost that inflated annual profits for the Omaha conglomerate.",
      "url": "https://www.wsj.com/articles/berkshire-hathaway-posted-29-billion-gain-in-2017-from-u-s-tax-plan-1519480047",
      "urlToImage": "https://si.wsj.net/public/resources/images/BN-XP717_3812B_TOP_20180224064100.jpg",
      "publishedAt": "2018-02-24T18:42:00Z",
      "digest":"3RjuEomJo26O1syZbU7OHA==\n",
      "reason": "Recommend"
    },
    {
      "source": "fortune",
      "title": "Here's How Much Bitcoin Elon Musk Owns",
      "description": "Tesla CEO Elon Musk isn’t exactly active in cryptocurrency. Musk revealed this week on Twitter how much Bitcoin he owns—and it’s not much.",
      "url": "http://fortune.com/2018/02/23/bitcoin-elon-musk-value/",
      "urlToImage": "https://fortunedotcom.files.wordpress.com/2018/01/elon-musk-tesla-silicon-valley-sex-party.jpg",
      "publishedAt": "2018-02-23T23:26:30Z",
      "digest":"3RjuEomJo26OadyZbU7OHA==\n",
      "reason": "Recommend"
    },
    {
      "source": "business-insider",
      "author": "Matthew DeBord",
      "title": "Elon Musk has no problem selling Tesla cars — but strong demand could become a problem",
      "description": "The temptation its to lump all of Tesla's problems together into one big problem bucket, mainly because the Model 3's delays have been so extreme.",
      "url": "http://www.businessinsider.com/tesla-strong-demand-could-backfire-become-problem-2018-2",
      "urlToImage": "https://amp.businessinsider.com/images/5a8f32db391d941d008b491a-750-375.jpg",
      "publishedAt": "2018-02-24T13:57:14Z",
      "digest":"3RjuEomJo2adf6OadyZbU7OHA==\n",
      "reason": "Today"
    },
    {
      "source": "Kotaku.com",
      "author": "Heather Alexandra",
      "title": "Riot Discloses Loot Box Odds For League of Legends",
      "description": "Riot Games revealed the drop rates for League of Legends’ loot crates yesterday, offering transparency for a system that until now has been opaque. This comes during a time when loot boxes have triggered a great deal of outrage among players, pundits, and eve…",
      "url": "https://kotaku.com/riot-discloses-loot-box-odds-for-league-of-legends-1823275409",
      "urlToImage": "https://i.kinja-img.com/gawker-media/image/upload/s--QS5t_zTw--/c_fill,fl_progressive,g_center,h_900,q_80,w_1600/j89vioglgrn74sdpzvez.png",
      "publishedAt": "2018-02-23T20:00:00Z",
      "digest":"3RjduEomJozf6OadyZbU7OHA==\n",
      "reason": "Today"
    }
    ];

    this.setState({news: mock_news});
  }

}

export default NewsPanel;
