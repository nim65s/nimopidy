import React from 'react';
import { Button, Glyphicon } from 'react-bootstrap';
import Progress from './progress';

class Volume extends React.Component {
  render() {
    return (
      <div>
        <h4>{this.props.name}</h4>
        <Button onClick={this.props.onMute} bsSize="large" className="pull-left">
          <Glyphicon glyph={this.props.muted ? 'volume-off' : 'volume-up'} />
        </Button>
        <Progress onSeek={this.props.onVolume} max={100} wheelCoef={.1} now={this.props.now} label={this.props.now} />
      </div>
    );
  }
}

export default Volume;
