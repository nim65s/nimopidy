import React from 'react';
import { Button, ButtonGroup, Glyphicon } from 'react-bootstrap';

class Controls extends React.Component {
  handlers(e) { this.props.handlers(e.target.name || e.target.parentElement.name); }

  render() {
    var handlers = this.handlers.bind(this);
    var disabled = !this.props.status;
    return (
      <ButtonGroup>
        <Button bsSize="lg" onClick={handlers} disabled={disabled} name="previous"><Glyphicon glyph="step-backward" /></Button>
        <Button bsSize="lg" onClick={handlers} disabled={disabled} name="play"    ><Glyphicon glyph="play"          /></Button>
        <Button bsSize="lg" onClick={handlers} disabled={disabled} name="pause"   ><Glyphicon glyph="pause"         /></Button>
        <Button bsSize="lg" onClick={handlers} disabled={disabled} name="stop"    ><Glyphicon glyph="stop"          /></Button>
        <Button bsSize="lg" onClick={handlers} disabled={disabled} name="next"    ><Glyphicon glyph="step-forward"  /></Button>
      </ButtonGroup>
    );
  }
}

export default Controls;
