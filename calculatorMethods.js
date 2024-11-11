function log(base, a){
    return Math.log(a) / Math.log(base);
}
function exponent(a, b){
    if (b == 0){
        return 1;
    }
    else{
        result = a;
        counter = 1;
        while (counter < b){
            result = result * a;
            counter = counter + 1;
        }
    }
    print("Result: " + result);
}
function absolute(a){
    if (a < 0){
        return -a;
    }
    else{
        return a;
    }
}
function generateEvens(lower, higher, fileName){
    if(lower % 2 ==0){
        lower += 2;
    } else {
        lower += 1;
    }
    evenNumbers = [lower];
    while (lower < higher){
        lower += 2;
        evenNumbers.push(lower);
    }
    File.open(fileName, "w");
    while (evenNumbers.length > 0){
        File.write(evenNumbers.pop());
    }
    print("File created.");
}
function generateSquares(lower, higher, fileName){
    squares = [];
    while (lower <= higher){
        squares.push(lower * lower);
        lower += 1;
    }
    File.open(fileName, "w");
    while (squares.length > 0){
        File.write(squares.pop());
    }
    print("File created.");
}
log(2, 8);
log(3, 9);
log(10, 100);

exponent(2, 3);
exponent(3, 0);
exponent(5, -2);

absolute(-5);
absolute(5);

generateEvens(1, 10, "evens.txt");
generateEvens(2, 20, "evens.txt");
generateEvens(3, 30, "evens.txt");

generateSquares(1, 10, "squares.txt");
generateSquares(2, 20, "squares.txt");
generateSquares(3, 30, "squares.txt");
