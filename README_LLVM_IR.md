# RoadRunner LLVM IR Access

This document explains how to access the LLVM IR (Intermediate Representation) that RoadRunner generates from SBML models.

## Overview

RoadRunner uses LLVM to compile SBML models into highly optimized machine code. The `getLLVMIR()` method allows you to inspect the LLVM IR that is generated, which shows you the mathematical equations and computational structure that RoadRunner creates from your SBML model.

## What is LLVM IR?

LLVM IR is a human-readable representation of the compiled code that shows:
- Mathematical equations derived from your SBML model
- Variable assignments and computations
- Function definitions for model evaluation
- Memory layout and data structures

## Building RoadRunner with LLVM IR Support

### Prerequisites

1. **LLVM Development Libraries**: Make sure you have LLVM development libraries installed
2. **CMake**: Version 3.16 or higher
3. **C++ Compiler**: GCC 7+, Clang 6+, or MSVC 2019+

### Build Steps

1. **Clone and configure**:
   ```bash
   git clone https://github.com/sys-bio/roadrunner.git
   cd roadrunner
   mkdir build && cd build
   cmake .. -DCMAKE_BUILD_TYPE=Release
   ```

2. **Build the project**:
   ```bash
   make -j$(nproc)  # On Windows: cmake --build . --config Release
   ```

3. **Install** (optional):
   ```bash
   make install
   ```

## Using the getLLVMIR() Method

### Python Example

```python
import roadrunner

# Create a RoadRunner instance with your SBML model
rr = roadrunner.RoadRunner("your_model.xml")

# Get the LLVM IR
llvm_ir = rr.getLLVMIR()

if llvm_ir:
    print("LLVM IR retrieved successfully!")
    print(f"IR size: {len(llvm_ir)} characters")
    print(llvm_ir)
else:
    print("No LLVM IR available")
```

### C++ Example

```cpp
#include "rrRoadRunner.h"

int main() {
    rr::RoadRunner rr("your_model.xml");
    
    std::string llvm_ir = rr.getLLVMIR();
    if (!llvm_ir.empty()) {
        std::cout << "LLVM IR:" << std::endl;
        std::cout << llvm_ir << std::endl;
    } else {
        std::cout << "No LLVM IR available" << std::endl;
    }
    
    return 0;
}
```

## Understanding the LLVM IR Output

The LLVM IR output contains several key sections:

### 1. Module Information
```
; ModuleID = 'roadrunner_model'
source_filename = "roadrunner_model"
target datalayout = "..."
```

### 2. Global Variables
```
@modelData = external global %struct.LLVMModelData
@globalParameters = global [1 x double] [double 0.100000e+00]
```

### 3. Function Definitions
```
define void @evalReactionRates(%struct.LLVMModelData* %modelData) {
  ; Function body with mathematical operations
}
```

### 4. Mathematical Operations
The IR shows how your SBML equations are translated:
- **Reaction rates**: `%rate = fmul double %k1, %species_concentration`
- **ODE equations**: `%dydt = fsub double %production, %consumption`
- **Assignment rules**: `store double %value, double* %variable`

## Example Output

For a simple model with reaction `A -> B` with rate `k1 * A`:

```llvm
define void @evalReactionRates(%struct.LLVMModelData* %modelData) {
entry:
  %0 = getelementptr inbounds %struct.LLVMModelData, %struct.LLVMModelData* %modelData, i32 0, i32 8
  %1 = load double*, double** %0
  %2 = getelementptr inbounds double, double* %1, i32 0
  %3 = load double, double* %2
  %4 = fmul double 0x3FB999999999999A, %3  ; k1 * A
  %5 = getelementptr inbounds %struct.LLVMModelData, %struct.LLVMModelData* %modelData, i32 0, i32 9
  %6 = load double*, double** %5
  %7 = getelementptr inbounds double, double* %6, i32 0
  store double %4, double* %7  ; Store reaction rate
  ret void
}
```

## Troubleshooting

### Common Issues

1. **"No LLVM IR available"**
   - The model might not be using the LLVM backend
   - Check that LLVM is properly linked
   - Ensure the model has been compiled successfully

2. **Build errors**
   - Verify LLVM development libraries are installed
   - Check CMake configuration
   - Ensure compatible compiler versions

3. **Empty IR output**
   - The model might be too simple or empty
   - Check that your SBML model is valid
   - Verify the model contains reactions and species

### Debug Information

To get more detailed information about the compilation process:

```python
import roadrunner
rr = roadrunner.RoadRunner("model.xml")
print(rr.getInfo())  # Shows model information
print(rr.getCompiler().getCompiler())  # Shows compiler being used
```

## Advanced Usage

### Custom Compiler Options

You can configure the LLVM compiler options:

```python
rr = roadrunner.RoadRunner()
rr.setCompiler("llvm")  # Ensure LLVM backend is used
# Load your model
llvm_ir = rr.getLLVMIR()
```

### Performance Analysis

The LLVM IR can help you understand:
- How your equations are optimized
- Memory access patterns
- Computational complexity
- Potential bottlenecks

## Contributing

If you encounter issues or want to improve the LLVM IR functionality:

1. Check the existing issues on GitHub
2. Create a minimal example that reproduces the problem
3. Include the LLVM IR output in your bug report
4. Test with different SBML models

## References

- [LLVM Documentation](https://llvm.org/docs/)
- [RoadRunner Documentation](https://roadrunner.readthedocs.io/)
- [SBML Specification](http://sbml.org/) 