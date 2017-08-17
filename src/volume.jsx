import React from 'react';
import { Button, Glyphicon } from 'react-bootstrap';
import Progress from './progress';

class Volume extends React.Component {
  render() {
    return (
      <p>
        <Button onClick={this.props.onMute} bsSize="large" className="pull-left">
          <Glyphicon glyph={this.props.muted ? 'volume-off' : 'volume-up'} /> {this.props.name}
        </Button>
        <Progress onSeek={this.props.onVolume} max={100} wheelCoef={.1} now={this.props.now} label={this.props.now} />
      </p>
      );
}
}

export default Volume;
