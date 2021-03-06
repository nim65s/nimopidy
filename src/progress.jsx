import React from 'react';
import { ProgressBar } from 'react-bootstrap';

class Progress extends React.Component {
  click(event) {
    var element = (event.target.parentElement.classList[0] === "progress" ? event.target.parentElement : event.target);
    var rectangle = element.getBoundingClientRect();
    this.props.onSeek(Math.round((event.pageX - rectangle.left) * this.props.max / rectangle.width));
  }

  wheel(e) {
    e.preventDefault();
    this.props.onSeek(Math.round(this.props.now - e.deltaY * this.props.wheelCoef));
  }

  render() {
    return (
      <ProgressBar onClick={this.click.bind(this)} onWheel={this.wheel.bind(this)}
        active={this.props.active} max={this.props.max} now={this.props.now} label={this.props.label}
      />
    );
  }
}

export default Progress;
