var app = angular.module('refearn', []);
app.controller('refearnController', function($scope, $http){
    $scope.addReferral = function(){
        $http.get('/api/customer/'+$scope.customer+'/?referrer='+$scope.referrer)
        .then(function onSuccess(response) {
            window.location.href = 'http://localhost:8000/api/customer/'+$scope.customer;
        }).catch(function onError(response) {
            console.log(response.data)
            alert(response.data.detail)
        });
    }
    $scope.addAmbassodor = function(){
        var doj = new Date($scope.joining_date)
        doc = doj.getFullYear()+"-"+(doj.getMonth()+1)+"-"+doj.getDate()
        var data = {email: $scope.email, joining_date:doc, referral_id:$scope.referral_id, is_ambassador:true}
        $http.post('/api/customer/', data)
        .then(function onSuccess(response) {
            window.location.href = 'http://localhost:8000/api/customer/';
        }).catch(function onError(response) {
            alert(response.data.status.toUpperCase()+" : "+response.data.response)
        });
    }
})