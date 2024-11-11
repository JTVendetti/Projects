# Category 1 #1
# JT Vendetti
def log(base, a)
  puts "Log base #{base} of #{a} is #{Math.log(a, base)}"
end
# Category 2
def exponent(a, b)
  # Raised to 0th power = 1
  if b == 0
    result = 1
  else
    result = a
    counter = 1
    # Loop to value of exponent and multiple to mimic behavior
    while counter < b
      result = result * a
      counter += 1
    end
  end
puts "#{a} raised to the power of #{b} equals #{result}"
end
# Find lower and upper bounds
def generateEven(lower, higher, fileName)
  if lower % 2 == 0
    lower = lower + 2
  elsif lower % 2 == 1
    lower = lower + 1
  end
  evenNumbers = [lower]
  # Add to array
  while lower < higher
    lower = lower + 2
    evenNumbers << lower
  end
  # Write to file
  File.open(fileName, 'w') do |file|
    evenNumbers.each { |num| file.puts num }
  end
  puts "Even numbers between #{lower} and #{higher} have been saved to #{fileName}."
end
# Absolute value changes negative to positive
def absolute(a)
  if a < 0
    absolute = a * -1
  else
    absolute = a
  end
  puts "The absolute value of #{a} is #{absolute}"
end
# Add squared number to array
def generateSquares(lower, higher, fileName)
  squares = []
  while lower <= higher
    squares << lower * lower
    lower = lower + 1
  end
  #Write to file
  File.open(fileName, 'w') do |file|
    squares.each { |num| file.puts num }
  end
end
# Testing functions by calling them
log(2, 8)
log(10, 100)
log(1, 0)

exponent(3, 4)
exponent(3, 0)
exponent(3, -2)
exponent(0, 4)

generateEven(15, 30, "even_numbers.txt")

absolute(-190)
absolute(190)

generateSquares(1, 10, "square_numbers.txt")
