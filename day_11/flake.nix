{
  description = "A C++ environment for UoA ADDS Projects";

  inputs = {
    nixpkgs.url = "nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = import nixpkgs { inherit system; };

      in
      {
  devShells.default = pkgs.mkShell.override {stdenv = pkgs.llvmPackages.stdenv;} {
          name = "adds";
          packages = with pkgs;
            [
              clang-tools
#        darwin.CarbonHeaders
#        darwin.apple_sdk.frameworks.Cocoa
#        darwin.apple_sdk.frameworks.IOKit
#        darwin.apple_sdk.frameworks.Kernel
            ];
        };
      }
    );
}
