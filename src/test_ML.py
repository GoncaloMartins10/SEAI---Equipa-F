from imports.HI_calculation.algorithms.method_5 import training, inference

perf=training(debug=True)
print(perf)
pred=inference(debug=True)
print(pred)

# Show tensorboard
# tensorboard --logdir logs/fit