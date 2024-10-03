{
  description = "PyOperon development environment";

  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    foolnotion.url = "github:foolnotion/nur-pkg";
    lbfgs.url = "github:foolnotion/lbfgs";
    nixpkgs.url = "github:nixos/nixpkgs/master";
    operon.url = "github:heal-research/operon/better-ownership-semantics";
    pratt-parser.url = "github:foolnotion/pratt-parser-calculator";
    vstat.url = "github:heal-research/vstat";

    foolnotion.inputs.nixpkgs.follows = "nixpkgs";
    lbfgs.inputs.nixpkgs.follows = "nixpkgs";
    operon.inputs.nixpkgs.follows = "nixpkgs";
    pratt-parser.inputs.nixpkgs.follows = "nixpkgs";
    vstat.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = inputs@{ self, flake-parts, nixpkgs, foolnotion, pratt-parser, lbfgs, vstat, operon }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [ "x86_64-linux" "aarch64-darwin" ];

      perSystem = { pkgs, system, ... }:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [
              foolnotion.overlay
              (final: prev: {
                vstat = vstat.packages.${system}.default;
              })
            ];
          };
          enableShared = false;
          stdenv_ = pkgs.llvmPackages_18.stdenv;
          python_ = pkgs.python3;
          operon_ = if enableShared then operon.packages.${system}.library else operon.packages.${system}.library-static;

          pythonPkgs = pkgs.python3Packages.override {
            overrides = self: super: {
              nanobind = super.nanobind.overridePythonAttrs (old: {
                doCheck = false;
                build-system = old.build-system ++ [ pythonPkgs.typing-extensions ];
                src = pkgs.fetchFromGitHub {
                  owner = "wjakob";
                  repo = "nanobind";
                  rev = "c1bab7e4207566b75bbc51c35079f66ae6f0afc0";
                  hash = "sha256-KaGSHt6dNR4vpCkU/rJIQuwFs3e8S4afpyCcabiBM8w=";
                  fetchSubmodules = true;
                };
              });
            };
          };
          nanobind = pythonPkgs.nanobind;


          pyoperon = stdenv_.mkDerivation {
            name = "pyoperon";
            src = self;

            cmakeFlags = [
              "--preset ${if pkgs.stdenv.hostPlatform.isx86_64 then "build-linux" else "build-osx"}"
            ];

            nativeBuildInputs = with pkgs; [
              cmake
              ninja
              pkg-config
              python_
              python_.pkgs.pybind11
            ];

            buildInputs = with pkgs; [
              (python_.withPackages (ps: with ps; [ setuptools wheel requests nanobind ]))
              operon_
            ] ++ operon_.buildInputs;
          };
        in
        rec {
          packages = {
            default = pyoperon;
            pyoperon-generic = pyoperon.overrideAttrs (old: {
              cmakeFlags = [
                "-DCMAKE_BUILD_TYPE=Release"
                "-DCMAKE_CXX_FLAGS=${
                  if pkgs.hostPlatform.isx86_64 then "-march=x86-64" else ""
                }"
              ];
            });
            pyoperon-debug = pyoperon.overrideAttrs
              (old: { cmakeBuildType = "Debug"; });
          };

          devShells.default = stdenv_.mkDerivation {
            name = "pyoperon-dev";
            nativeBuildInputs = pyoperon.nativeBuildInputs;
            buildInputs = pyoperon.buildInputs;
          };

          devShells.pyenv = stdenv_.mkDerivation {
            name = "pyoperon-dev";
            nativeBuildInputs = pyoperon.nativeBuildInputs;
            buildInputs = pyoperon.buildInputs ++ (with pkgs; [ gdb valgrind gcc13 pkgs.vstat ])
              ++ (with python_.pkgs; [ scikit-build ]) # cmake integration and release preparation
              ++ (with python_.pkgs; [ numpy scikit-learn pandas pyarrow ipdb sympy requests matplotlib optuna jax jaxlib-bin torch ])
              ++ (with pkgs; [ (pmlb.override { pythonPackages = python_.pkgs; }) ]);
          };
        };
    };
}
