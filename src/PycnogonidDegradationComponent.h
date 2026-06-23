#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "PhysicsEngine/PhysicsConstraintComponent.h"
#include "PycnogonidDegradationComponent.generated.h"

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class METASTASISTRACKERAI_API UPycnogonidDegradationComponent : public UActorComponent
{
    GENERATED_BODY()

public:    
    UPycnogonidDegradationComponent();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chemical Degradation")
    float OptimalPH;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chemical Degradation")
    float AlkalineDegradationK;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chemical Degradation")
    float AlkalineExponentB;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chemical Degradation")
    float AcidDegradationK;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chemical Degradation")
    float AcidExponentA;

    UPROPERTY(BlueprintReadOnly, Category = "Chemical Degradation")
    float StructuralIntegrity;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Physics Assembly")
    TArray<UPhysicsConstraintComponent*> JointConstraints;

    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

private:
    float GetWorldEnvironmentPH();
    void TriggerTotalStructuralLiquefaction();
};
