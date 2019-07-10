import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Header from './components/Header';
import Main from './components/Main';

class App extends Component {
  render() {
    return(
      <React.Fragment>
        <Header />
        <Main />
      </React.Fragment>
    );
  }
}

ReactDOM.render(<App />, document.getElementById('root'));
