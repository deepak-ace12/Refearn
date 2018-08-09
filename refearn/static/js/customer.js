var app = angular.module('refearn', []);
app.controller('refearnController', function($scope, $http){
    //$scope.todoList = [{todoText: 'Finish This App', done:false}];

    // $http.get('/api/customer').then(function(response){
    //     $scope.todoList = [];
    //     for(var i=0; i<response.data.length; i++){
    //         console.log('here')
    //         var todo = {};
    //         todo.todoText = response.data[i].text;
    //         todo.done = response.data[i].done;
    //         todo.id = response.data[i].id;
    //         $scope.todoList.push(todo);
    //     }
    // });
    $scope.saveData = function(){
        $http.put('/api/customer/'+$scope.customer+'/?referrer='+$scope.referrer)
    }

    $scope.getAllCustomers = function(){
        $http.get('/api/customer/')
    }
    $scope.getCustomer = function(id){
        $http.get('/api/customer/'+id)
    }

    // $scope.todoAdd = function(){
    //     $scope.todoList.push({todoText: $scope.todoInput, done:false});
    //     $scope.todoInput = '';
    // };

    // $scope.remove = function(){
    //     var oldList = $scope.todoList;
    //     $scope.todoList = [];
    //     angular.forEach(oldList, function(todo){
    //         if(todo.done) {
    //             $http.delete('/todo/api/'+ todo.id +'/');
    //         } else {
    //             $scope.todoList.push(todo);
    //         }
    //     })

    // }
})