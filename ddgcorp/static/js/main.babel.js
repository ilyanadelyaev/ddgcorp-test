// CSRF token for AJAX

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    }
});


// Drag-n-Drop

var DRAG_THRESHOLD = 3;  // pixels

var Draggable = React.createClass({
    // Cover object to Draggable to drag-n-drop it on DropTarget
    // CSS: dnd-draggable / dnd-draggable.dragging
    // props: 
    // * onDragStart - process drag start by parent
    // * onDragStop - process drag stop by parent
    // * dragID - to identify child object

    // handlers
    onMouseEnter: function(e) {
        this.setState({hover: true});
    },

    onMouseLeave: function(e) {
        this.setState({hover: false});
    },

    onMouseDown: function(e) {
        if ( e.button === 0 ) {  // left button
            e.stopPropagation();
            e.preventDefault();
            this.addEvents();

            var currentRect = ReactDOM.findDOMNode(this).getBoundingClientRect();
            var parrentRect = ReactDOM.findDOMNode(this).parentNode.getBoundingClientRect();

            this.setState({
                mouseDown: true,
                width: currentRect.width,
                height: currentRect.height,
                originX: e.pageX,
                originY: e.pageY,
                elementX: currentRect.left - parrentRect.left,
                elementY: currentRect.top - parrentRect.top
            });
        }
    },

    onMouseMove: function(e) {
        var deltaX = e.pageX - this.state.originX;
        var deltaY = e.pageY - this.state.originY;
        var distance = Math.abs(deltaX) + Math.abs(deltaY);

        if ( ( ! this.state.dragging ) && ( distance > DRAG_THRESHOLD ) ) {
            this.setState({dragging: true});
            this.props.onDragStart && this.props.dragID && this.props.onDragStart(this.props.dragID());
        }

        if ( this.state.dragging ) {
            e.stopPropagation();
            e.preventDefault();
            this.setState({
                left: this.state.elementX + deltaX + document.body.scrollLeft,
                top: this.state.elementY + deltaY + document.body.scrollTop
            });
        }
    },

    onMouseUp: function(e) {
        this.removeEvents();
        if ( this.state.dragging ) {
            this.setState({dragging: false});
            this.props.onDragStop && this.props.onDragStop();
        }
    },

    // Init

    getInitialState: function() {
        return {
            mouseDown: false,
            dragging: false,
            hover: false
        };
    },

    // Tools

    addEvents: function() {
        document.addEventListener('mousemove', this.onMouseMove);
        document.addEventListener('mouseup', this.onMouseUp);
    },

    removeEvents: function() {
        document.removeEventListener('mousemove', this.onMouseMove);
        document.removeEventListener('mouseup', this.onMouseUp);
    },

    style: function() {
        if ( this.state.dragging ) {
            return {
                position: 'absolute',
                zIndex: 100,
                left: this.state.left,
                top: this.state.top,
                width: this.state.width,  // because absolute
                height: this.state.height  // because absolute
            };
        } else {
            return {};
        }
    },

    // Draw

    render: function() {
        // classNames
        var classes = classNames({
            'dnd-draggable': true,
            'dragging': this.state.dragging,
            'hover': this.state.hover
        });
        // draw
        return (
            <div
                className={classes}
                style={this.style()}
                children={this.props.children}
                onMouseDown={this.onMouseDown}
                onMouseEnter={this.onMouseEnter}
                onMouseLeave={this.onMouseLeave}
            />
        );
    }
});


var DropTarget = React.createClass({
    // Cover Object to DropTarget for catch Draggable
    // CSS: dnd-drop-target / dnd-drop-target.hover
    // props:
    // * onDrop - process drop by parent
    // * dropID - to identify child object

    // handlers
    onDrop: function(e) {
        this.props.onDrop && this.props.dropID && this.props.onDrop(this.props.dropID());
    },
    //
    onMouseEnter: function(e) {
        this.mouseHover(true);
    },
    onMouseLeave: function(e) {
        this.mouseHover(false);
    },
    mouseHover: function(hover) {
        this.setState({hover: hover});
        this.props.mouseHover && this.props.mouseHover(hover);
    },
    //
    getInitialState: function() {
        return {
            hover: false
        };
    },
    //
    render: function() {
        // classNames
        var classes = classNames({
            'dnd-drop-target': true,
            'hover': this.state.hover
        });
        //
        return (
            <div
                className={classes}
                children={this.props.children}
                onMouseEnter={this.onMouseEnter}
                onMouseLeave={this.onMouseLeave}
                onMouseUp={this.onDrop}
            />
        );
    }
});


// Board

var Task = React.createClass({
    // Using Draggable mixin
    // CSS: ddgcorp-task

    // drag data
    dragID: function() {
        return {
            id: this.props.task.id,
            list_id: this.props.list_id,
            el_id: this.elID()
        };
    },

    // tools
    elID: function() {
        return 'task-' + this.props.task.id;
    },

    // draw
    render: function() {
        return (
            <Draggable
                onDragStart={this.props.onDragStart}
                onDragStop={this.props.onDragStop}
                dragID={this.dragID}
            >
                <div
                    id={this.elID()}
                    className="ddgcorp-task"
                >
                    {this.props.task.name}
                </div>
            </Draggable>
        );
    }
});

var TasksList = React.createClass({
    // Store tasks here
    // Using as DropTarget
    // CSS: ddgcorp-taskslist + col-md-2

    // D-n-D callback on mouse hover
    mouseHover: function(hover) {
        this.setState({hover: hover});
    },

    // D-n-D identifier
    dropID: function() {
        return {
            id: this.props.tasks_list.id,
            el_id: this.elID()
        };
    },

    getInitialState: function() {
        return {
            hover: false,
        };
    },

    // tools
    elID: function() {
        return 'tasks-list-' + this.props.tasks_list.id;
    },

    // draw
    render: function() {
        // drop place
        var drop_place = '';
        if ( this.props.dragging() && this.state.hover ) {
            drop_place = (
                <div className='dnd-drop-place'/>
            );
        }
        // tasks list
        var tasks = '';
        var _this = this;  // declare locally
        tasks = this.props.tasks_list.tasks.map(function(task) {
            return (
                <Task
                    key={task.id}
                    list_id={_this.props.tasks_list.id}
                    task={task}
                    onDragStart={_this.props.onDragStart}
                    onDragStop={_this.props.onDragStop}
                />
            );
        });
        // create list with DropTarget mixin
        return (
            <DropTarget
                dropID={this.dropID}
                onDrop={this.props.onDrop}
                mouseHover={this.mouseHover}
            >
                <div
                    id={this.elID()}
                    className='ddgcorp-taskslist col-md-2'
                    onMouseEnter={this.handleMouseEnter}
                    onMouseLeave={this.handleMouseLeave}
                >
                    <div
                        className="ddgcorp-statuslabel"
                    >
                        {this.props.tasks_list.name}
                    </div>
                    {drop_place}
                    {tasks}
                </div>
            </DropTarget>
        );
    }
});

var Board = React.createClass({
    // Process D-n-D here
    // Make server requests here
    // Create and update board configuration here
    // Process WebSockets
    // CSS: ddgcorp-board + row

    // D-n-D handlers

    onDragStart: function(data) {
        this.setState({current_drag_item: data});
    },

    onDragStop: function() {
        this.setState({current_drag_item: null});
    },

    dragging: function() {
        return ! ! this.state.current_drag_item;
    },

    onDrop: function(data) {
        // update board configuration and send server update request
        //
        if ( ! this.state.current_drag_item )
            return;
        //
        var tasks = this.state.tasks;
        var statuses = this.state.statuses;
        //
        var task_id = this.state.current_drag_item.id;
        var new_status = statuses[data.id];
        // update task status
        tasks[task_id].status_id = new_status.id;
        //
        //this.setState({tasks: tasks});
        // send update request to server
        this.updateTaskStatus(task_id, new_status.id);
    },

    // WebSockets

    wsRegisterHandler: function() {
        // relative ws uri
        var loc = window.location;
        var uri = '';
        if (loc.protocol === 'https:') {
            uri = 'wss:';
        } else {
            uri = 'ws:';
        }
        uri += '//' + loc.host;
        uri += '/ws/models?subscribe-broadcast';
        //
        var ws_handler = WS4Redis({
            uri: uri,
            receive_message: this.wsMessageRecieved,
            heartbeat_msg: '--heartbeat--'
        });
        this.setState({ws_handler: ws_handler});
    },

    wsMessageRecieved: function(data) {
        if ( ! this.state.statuses || ! this.state.tasks )
            return;
        data = JSON.parse(data);
        if ( ! data.model )
            return;
        switch ( data.type ) {
            case 'status':
                if ( data.action == 'save' ) {
                    this.state.statuses[data.model.id] = data.model;
                } else if ( data.action == 'delete' ) {
                    delete this.state.statuses[data.model.id];
                }
                this.setState({statuses: this.state.statuses});
                break;
            case 'task':
                if ( data.action == 'save' ) {
                    this.state.tasks[data.model.id] = data.model;
                } else if ( data.action == 'delete' ) {
                    delete this.state.tasks[data.model.id];
                }
                this.setState({tasks: this.state.tasks});
                break;
        }
    },

    // Server comunication

    fetchStatuses: function() {
        var url = '/api/status/';
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            cache: false,
            success: function(data) {
                var statuses = this.convertStatuses(data);
                this.setState({statuses: statuses});
                // load tasks
                this.fetchTasks();
            }.bind(this),
            error: function(xhr, status, err) {
                // show error
                console.error(url, status, err.toString());
            }.bind(this)
        });
    },

    fetchTasks: function() {
        var url = '/api/task/';
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            cache: false,
            success: function(data) {
                var tasks = this.convertTasks(data);
                this.setState({tasks: tasks});
            }.bind(this),
            error: function(xhr, status, err) {
                // show error
                console.error(url, status, err.toString());
            }.bind(this)
        });
    },

    updateTaskStatus: function(task_id, new_status_id) {
        // send new task status to server
        var url = '/api/task/' + task_id + '/status/';
        $.ajax({
            url: url,
            type: 'PUT',
            dataType: 'json',
            data: JSON.stringify({
                status: new_status_id,
            }),
            error: function(xhr, status, err) {
                // TODO: show error
                console.error(url, status, err.toString());
            }.bind(this)
        });
    },

    // Init

    getInitialState: function() {
        return {
            statuses: null,
            tasks: null,
            current_drag_item: null,
        };
    },

    componentDidMount: function() {
        // init from server
        this.fetchStatuses();
        // register ws
        this.wsRegisterHandler();
    },

    componentWillUnmount: function() {
    },

    // Tools

    convertStatuses: function(data) {
        var statuses = {};
        data.map(function(status) {
            statuses[status.id] = status;
        });
        return statuses;
    },

    convertTasks: function(data) {
        var tasks = {};
        data.map(function(task) {
            tasks[task.id] = task;
        });
        return tasks;
    },

    getBoardConfig: function() {
        var tasks = this.state.tasks;
        var statuses = this.state.statuses;
        if ( ! tasks || ! statuses )
            return;
        //
        var board_config = {};
        // statuses
        for ( var s in statuses ) {
            var status = statuses[s];
            board_config[status.id] = {
                'id': status.id,
                'name': status.name,
                'tasks': []
            };
        }
        // tasks
        for ( var t in tasks ) {
            var task = tasks[t];
            if ( task.status_id in board_config )
                board_config[task.status_id].tasks.push(task);
        }
        //
        return board_config;
    },

    // Draw

    render: function() {
        var board_config = this.getBoardConfig();
        // create tasks_lists
        var lists = [];
        if ( board_config ) {
            var _this = this;  // declare locally
            for ( var s in board_config ) {
                var tasks_list = board_config[s];
                lists.push(
                    <TasksList
                        key={tasks_list.id}
                        tasks_list={tasks_list}
                        onDragStart={_this.onDragStart}
                        onDragStop={_this.onDragStop}
                        onDrop={_this.onDrop}
                        dragging={_this.dragging}
                    />
                );
            }
        }
        // create board
        return (
            <div
                className="ddgcorp-board row"
                onDragStart={this.onDragStart}
                onDragStop={this.onDragStop}
            >
                {lists}
            </div>
        );
    }
});


// Run

var mountNode = document.getElementById('content');
ReactDOM.render(<Board/>, mountNode);
