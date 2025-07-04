#!/usr/bin/env python3
"""
Example script demonstrating how to get LLVM IR from RoadRunner.
This script shows the LLVM IR that RoadRunner generates for SBML models.
"""

import roadrunner

def main():
    # Create a simple SBML model (you can replace this with your own model)
    sbml = """<?xml version="1.0" encoding="UTF-8"?>
<sbml xmlns="http://www.sbml.org/sbml/level3/version1/core" level="3" version="1">
  <model id="example_model">
    <listOfCompartments>
      <compartment id="cell" size="1"/>
    </listOfCompartments>
    <listOfSpecies>
      <species id="A" compartment="cell" initialConcentration="1.0"/>
      <species id="B" compartment="cell" initialConcentration="0.0"/>
    </listOfSpecies>
    <listOfParameters>
      <parameter id="k1" value="0.1"/>
    </listOfParameters>
    <listOfReactions>
      <reaction id="R1" reversible="false">
        <listOfReactants>
          <speciesReference species="A" stoichiometry="1"/>
        </listOfReactants>
        <listOfProducts>
          <speciesReference species="B" stoichiometry="1"/>
        </listOfProducts>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <apply>
              <times/>
              <ci>k1</ci>
              <ci>A</ci>
            </apply>
          </math>
        </kineticLaw>
      </reaction>
    </listOfReactions>
  </model>
</sbml>"""
    
    try:
        # Create RoadRunner instance
        r = roadrunner.RoadRunner(sbml)
        
        print("✅ RoadRunner instance created successfully!")
        print(f"Model: {r.getModelName()}")
        print(f"Species: {r.getNumFloatingSpecies()}")
        print(f"Reactions: {r.getNumReactions()}")
        
        # Get the LLVM IR
        print("\n" + "="*60)
        print("LLVM IR (showing the generated equations):")
        print("="*60)
        
        llvm_ir = r.getLLVMIR()
        if llvm_ir:
            print("✅ LLVM IR retrieved successfully!")
            print(f"IR size: {len(llvm_ir)} characters")
            print("\nLLVM IR content:")
            print("-" * 40)
            print(llvm_ir)
        else:
            print("❌ No LLVM IR available")
            print("This might happen if:")
            print("  - The model is not using the LLVM backend")
            print("  - The model hasn't been compiled yet")
            print("  - There was an error during compilation")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure RoadRunner is properly installed")
        print("2. Check that your SBML model is valid")
        print("3. Ensure you have the latest version of RoadRunner")

if __name__ == "__main__":
    main() 