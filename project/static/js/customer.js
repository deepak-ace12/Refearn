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
    $scope.addReferral = function(){
        $http.put('/api/customer/'+$scope.customer+'/?referrer='+$scope.referrer)
    }

    $scope.addAmbassodor = function(){
        var doj = new Date($scope.joining_date)
        // var month = format(todayTime .getMonth() + 1);
        // var day = format(todayTime .getDate());
        // var year = format(todayTime .getFullYear());
        doc = doj.getFullYear()+"-"+(doj.getMonth()+1)+"-"+doj.getDate()
        var data = {email: $scope.email, joining_date:doc, referral_id:$scope.referral_id, is_ambassador:true}
        $http.post('/api/customer/', data)
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