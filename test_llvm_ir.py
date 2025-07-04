#!/usr/bin/env python3
"""
Test script to demonstrate the getLLVMIR() functionality in RoadRunner.
"""

import roadrunner

def test_get_llvm_ir():
    """Test the getLLVMIR() method with a simple SBML model."""
    
    # Create a simple SBML model
    sbml = """<?xml version="1.0" encoding="UTF-8"?>
<sbml xmlns="http://www.sbml.org/sbml/level3/version1/core" level="3" version="1">
  <model id="simple_model">
    <listOfCompartments>
      <compartment id="compartment" size="1"/>
    </listOfCompartments>
    <listOfSpecies>
      <species id="S1" compartment="compartment" initialConcentration="1"/>
      <species id="S2" compartment="compartment" initialConcentration="0"/>
    </listOfSpecies>
    <listOfReactions>
      <reaction id="R1" reversible="false">
        <listOfReactants>
          <speciesReference species="S1" stoichiometry="1"/>
        </listOfReactants>
        <listOfProducts>
          <speciesReference species="S2" stoichiometry="1"/>
        </listOfProducts>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <apply>
              <times/>
              <ci>k1</ci>
              <ci>S1</ci>
            </apply>
          </math>
          <listOfParameters>
            <parameter id="k1" value="0.1"/>
          </listOfParameters>
        </kineticLaw>
      </reaction>
    </listOfReactions>
  </model>
</sbml>"""
    
    try:
        # Create RoadRunner instance
        rr = roadrunner.RoadRunner(sbml)
        
        print("RoadRunner instance created successfully!")
        print(f"Model name: {rr.getModelName()}")
        print(f"Number of species: {rr.getNumFloatingSpecies()}")
        print(f"Number of reactions: {rr.getNumReactions()}")
        
        # Get the LLVM IR
        print("\n" + "="*50)
        print("LLVM IR:")
        print("="*50)
        
        llvm_ir = rr.getLLVMIR()
        if llvm_ir:
            print("LLVM IR retrieved successfully!")
            print(f"IR length: {len(llvm_ir)} characters")
            print("\nFirst 1000 characters of LLVM IR:")
            print("-" * 30)
            print(llvm_ir[:1000])
            if len(llvm_ir) > 1000:
                print("... (truncated)")
        else:
            print("No LLVM IR available (possibly not an LLVM model)")
            
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Testing RoadRunner getLLVMIR() functionality...")
    success = test_get_llvm_ir()
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!") 