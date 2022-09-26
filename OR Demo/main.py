import math
import gurobipy as gp
from gurobipy import GRB
from flask import Flask, render_template, url_for, request
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
  result = False
  if request.method == 'POST':
    form = request.form
    result = calculate(form)
  return render_template('index.html', result=result)


def calculate(form):
  c1 = int(request.form['c1'])
  c2 = int(request.form['c2'])
  c3 = int(request.form['c3'])
  result = model(c1,c2,c3)
  return result 
  
def model(c1,c2,c3):
  # Create a new model
  m = gp.Model("bilinear")

    # Create variables
  x = m.addVar(name="x")
  y = m.addVar(name="y")


  # Set objective: maximize x
  m.setObjective(5.0*x + 7.0*y, GRB.MAXIMIZE)

  # Add linear constraint: x  <= 6

  m.addConstr(x  <= c1, "c1")

  # Add bilinear inequality constraint: 3x + 4y <= 24
  m.addConstr(3*x + 4*y <= c2, "c2")

  # Add bilinear equality constraint: x * z + y * z == 7
  m.addConstr(x+ y <= c3, "c3")


  # First optimize() call will fail - need to set NonConvex to 2
  try:
      m.optimize()
  except gp.GurobiError:
      print("Optimize failed due to non-convexity")

  # Solve bilinear model
  m.Params.NonConvex = 2
  m.optimize()

  a = m.getObjective()
  return (a.getValue())
  
  # # Constrain 'x' to be integral and solve again
  # x.VType = GRB.INTEGER
  # m.optimize()
  # return m.printAttr('x')


if __name__ == "__main__":
  app.run(debug=True)
  