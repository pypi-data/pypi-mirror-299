#pragma once

#include "flux_density.h"
#include "particle_generator.h"
#include "coherent_radiation.h"

class SeedLight;

class FELAmplifier :
	public CoherentRadiationBase
{
public:
	FELAmplifier(
		SpectraSolver &spsolver, Trajectory *trajectory, FilterOperation *filter, int fellayer);
	virtual ~FELAmplifier();
	void AdvanceSection(int nsec);
	virtual void GetValues(double *xyobsin, vector<double> *values);
	int GetSections(){return m_nsections;}
	int GetTotalSteps();
	void ArrangeObservation(double Dxy[], double dxy[]);
	void ArrangeEtGrid();
	void GetBunchInf(
		vector<double> &zstep,
		vector<double> &energy,
		vector<vector<vector<double>>> &bunchf,
		vector<double> &currt,
		vector<vector<double>> &currI
	);

private:
	int f_GetSteps(int tgtsec);
	void f_GetValues(double *xyobs, vector<double> &values, bool istime);
	void f_GetValuesTimeAt(vector<int> &nx, vector<int> &ny);
	void f_GetValuesFluxAt(vector<int> &nx, vector<int> &ny);
	void f_AdvanceParticles(int tgtsection);
	bool f_SetEtSpace(int Nmax);
	double f_GetCharge(Particle &particle, double dtE[]);
	double f_ElectronNumber(double t);
	void f_SetTime();
	void f_AdjustCharge();
	void f_GetBunchFactor(int tgtsection);
	void f_GetComplexAmpAt(int tgtindex, double *xyobs = nullptr, bool istime = true);
	void f_GetComplexAmpMB(int tgtindex, double *xyobs = nullptr);
	void f_GetComplexAmpSection(int srcindex, int tgtindex, double xy[]);
	void f_FreeWS();

	Trajectory *m_trajec;
	SeedLight *m_seed;
	FastFourierTransform *m_spfft;

	int m_nsections;
	double m_dxy[2];
	double m_dXY[2];
	double m_bmmax[2];
	double m_dt;
	int m_ngfft[2];
	int m_nghalf[2];
	double m_t0;
	double **m_ws;
	int m_fellayer;

	vector<Particle> m_particles;
	vector<double> m_charge;
	Particle m_reference;
	int m_Nparticles;

	vector<double> m_tgrid;
	vector<double> m_xygrid[2];
	vector<vector<double>> m_FxyGrid[4];
	vector<vector<double>> m_SxyGrid[4];
	vector<vector<vector<vector<double>>>> m_EtGrid;
	vector<vector<int>> m_secidx;
	vector<double> m_zorbit;
	vector<vector<double>> m_kick;
	vector<double> m_Zi;
	vector<double> m_tstep;
	vector<vector<double>> m_bmsize;
	vector<vector<vector<double>>> m_bunchf;

	vector<double> m_currt;
	vector<vector<double>> m_currI;

	vector<vector<vector<double>>> m_wsef;

	const int STEPSPARTICLES = 10000;
};

class SeedLight
{
public:
	SeedLight(double pkpower,
		double epcenter, double pulselenFWHM, double srcsizeFWHM,
		double zwaist, double torg);
	void GetAmplitudeS(double ep, double tshift, double zpos, double xy[], double Exy[]);
	void GetAmplitudeA(double ep, double tshift, double zpos, double kxy[], double Exy[]);

private:
	double f_GetAmp(double ep, double tex);
	double m_E0;
	double m_sigmat;
	double m_Epk;
	double m_epcenter;
	double m_zrayl;
	double m_sigmath;
	double m_sigmaxy;
	double m_torg;
	double m_zwaist;
};
