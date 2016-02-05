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
    onMouseDown: function(e) {
        if ( e.button == 0 ) {  // left button
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
    //
    addEvents: function() {
        document.addEventListener('mousemove', this.onMouseMove);
        document.addEventListener('mouseup', this.onMouseUp);
    },
    removeEvents: function() {
        document.removeEventListener('mousemove', this.onMouseMove);
        document.removeEventListener('mouseup', this.onMouseUp);
    },
    //
    getInitialState: function() {
        return {
            mouseDown: false,
            dragging: false
        }
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
            }
        } else {
            return {}
        }
    },
    render: function() {
        // classNames
        var classes = classNames({
            'dnd-draggable': true,
            'dragging': this.state.dragging
        });
        // draw
        return (
            <div
                className={classes}
                style={this.style()}
                onMouseDown={this.onMouseDown}
                children={this.props.children}
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
        this.props.onDrop && this.props.dropID && this.props.onDrop(this.props.dropID())
    },
    //
    onMouseEnter: function(e) {
        this.setState({hover: true});
    },
    onMouseLeave: function(e) {
        this.setState({hover: false});
    },
    //
    getInitialState: function() {
        return {
            hover: false
        }
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
        }
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
    mouseHoverState: function(hover) {
        this.setState({hover: hover});
    },

    // D-n-D identifier
    dropID: function() {
        return {
            id: this.props.tasks_list.id,
            el_id: this.elID()
        }
    },

    // tools
    elID: function() {
        return 'tasks-list-' + this.props.tasks_list.id;
    },

    // draw
    render: function() {
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
    // CSS: ddgcorp-board + row

    // init
    getInitialState: function() {
        return {
            board_statuses: null,  // avaliable board statuses to create board
            board: null,  // board configuration
            current_drag_item: null,
            update_timer: null,
            last_modified: 0  // timestamp
        }
    },

    // D-n-D handlers
    onDragStart: function(data) {
        this.setState({current_drag_item: data})
    },
    onDragStop: function() {
        this.setState({current_drag_item: null})
    },
    onDrop: function(data) {
        // update board configuration and send server update request
        //
        if ( ! this.state.current_drag_item )
            return
        //
        var board = this.state.board;
        var board_statuses = this.state.board_statuses;
        //
        var task_id = this.state.current_drag_item.id;
        var start_list_id = this.state.current_drag_item.list_id;
        var end_list_id = data.id;
        var task = board[start_list_id].tasks[task_id];
        // update configuration
        delete board[start_list_id].tasks[task_id];
        // create board list if needed
        if ( ! ( end_list_id in board ) ) {
            board[end_list_id] = {
                id: end_list_id,
                name: this.state.board_statuses[end_list_id].name,
                tasks: []
            }
        }
        // insert into list
        board[end_list_id].tasks[task_id] = task;
        //
        //this.setState({board: board});
        // send update request to server
        this.updateTaskStatus(task_id, end_list_id);
    },

    // preprocess and load data
    componentDidMount: function() {
        this.loadStatuses();
        // set update timer
        if ( ! this.state.update_timer ) {
            this.setState({
                update_timer: setInterval(this.foregroundUpdater, 2000)
            });
        }
    },

    componentWillUnmount: function() {
        clearInterval(this.state.update_timer);
        this.setState({update_timer: null});
    },

    // fetch statuses
    loadStatuses: function() {
        var url = '/api/status/';
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            cache: false,
            success: function(data) {
                var board_statuses = {};
                data.map(function(o) {
                    board_statuses[o.id] = o;
                });
                this.setState({board_statuses: board_statuses});
                // load tasks
                this.loadTasks();
            }.bind(this),
            error: function(xhr, status, err) {
                // show error
                console.error(url, status, err.toString());
            }.bind(this)
        });
    },

    // fetch tasks
    loadTasks: function() {

        console.log('load');

        var url = '/api/task/';
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            cache: false,
            success: function(data) {
                var board = {};
                data.map(function(d) {
                    if ( ! ( d.status.id in board ) ) {
                        board[d.status.id] = {
                            id: d.status.id,
                            name: d.status.name,
                            tasks: {}
                        }
                    }
                    board[d.status.id].tasks[d.id] = d;
                });
                //
                this.setState({board: board});
            }.bind(this),
            error: function(xhr, status, err) {
                // show error
                console.error(url, status, err.toString());
            }.bind(this)
        });
    },

    checkModifiedAndUpdate: function() {
        var url = '/api/last_modified';
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            cache: false,
            success: function(data) {
                if ( data.timestamp != this.state.last_modified ) {
                    this.setState({last_modified: data.timestamp});
                    this.loadTasks();
                }
            }.bind(this),
            error: function(xhr, status, err) {
                // show error
                console.error(url, status, err.toString());
            }.bind(this)
        });
    },

    // foreground update board
    foregroundUpdater: function() {
        // dragging now? - skip update
        if ( this.state.current_drag_item )
            return;
        // update board
        this.checkModifiedAndUpdate();
    },

    // update task status
    updateTaskStatus: function(task_id, new_status_id) {
        // send new task status to server
        var url = '/api/task/' + task_id + '/status/';
        $.ajax({
            url: url,
            type: 'PUT',
            dataType: 'json',
            data: JSON.stringify({
                new_status_id: new_status_id,
            }),
            error: function(xhr, status, err) {
                // TODO: show error
                console.error(url, status, err.toString());
            }.bind(this)
        });
    },

    // tools
    getBoardConfiguration: function() {
        var board = this.state.board;
        var board_statuses = this.state.board_statuses;
        if ( ! board || ! board_statuses )
            return;
        //
        var ret = [];
        // collect all statuses
        for ( var s in board_statuses ) {
            var status = board_statuses[s];
            var tasks = [];
            if ( status.id in board ) {
                for (var t in board[status.id].tasks) {
                    tasks.push(board[status.id].tasks[t]);
                }
            }
            ret.push({
                id: status.id,
                name: status.name,
                tasks: tasks
            });
        }
        return ret;
    },

    // draw
    render: function() {
        var board_configuration = this.getBoardConfiguration();
        // create tasks_lists
        var lists = '';
        if ( board_configuration ) {
            var _this = this;  // declare locally
            lists = board_configuration.map(function(tasks_list) {
                return (
                    <TasksList
                        key={tasks_list.id}
                        tasks_list={tasks_list}
                        onDragStart={_this.onDragStart}
                        onDragStop={_this.onDragStop}
                        onDrop={_this.onDrop}
                    />
                );
            });
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


// run
var mountNode = document.getElementById('content');
ReactDOM.render(<Board/>, mountNode);
