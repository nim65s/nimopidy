import React from 'react';
import Progress from './progress';


class Snap extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      connected: false,
      now: 29
    }
  }

  render() {
    return <Progress now={this.state.now} />;
  }
}

export default Snap;
