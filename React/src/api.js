import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Fetch from './components/Fetch'

class App extends Component{
  render() {
      return(
        <React.Fragment>
          <Fetch />
        </React.Fragment>
      );
  }
}

ReactDOM.render(<App />, document.getElementById('root'));
